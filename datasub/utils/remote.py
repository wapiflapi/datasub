import graphql

from graphql.execution.base import get_field_entry_key


def default_merged_resolver(parent, info, **_kwargs):

    response_key = get_field_entry_key(info.field_asts[0])
    # get_errors_from_parent is supposed to be called here,
    # but I don't yet know what it should be doing.

    if parent is None:
        return None

    result = parent.get(response_key)
    if not result and 'data' in parent:
        result = parent['data'].get(response_key)

    return result


def typename_resolver(parent, info, **_kwargs):

    # Basically we can't resolve abstracts. That sucks.
    # we make sure it's explicit by requiring __typename.
    # It might be good to just merge all abstract types?
    # Or figure out which ones match?

    try:
        typename = parent['__typename']
    except KeyError:
        # This is a user error! make that clear.
        raise RuntimeError(
            "__typename not fetched for object, unable to resolve interface"
        )

    resolvedtype = info.schema.get_type(typename)
    if resolvedtype is None:
        raise RuntimeError(
            "__typename did not match an object type: %s" % typename
        )

    return resolvedtype


def create_sync_resolver(client):
    def resolver(parent, info, **_kwargs):
        definitions = [info.operation]
        definitions.extend(info.fragments.values())

        document = graphql.language.ast.Document(
            definitions=definitions,
        )

        result = client.execute(document)
        return default_merged_resolver(result, info)

    return resolver


def make_remote_executable_schema(schema, client):
    # Get a generic resolver for this client.
    sync_resolver = create_sync_resolver(client)

    # Get a deep copy of the schema by extending it with an empty ASST.
    noopdoc = graphql.language.ast.Document([])
    schema = graphql.extend_schema(schema, documentAST=noopdoc)

    query_type = schema.get_query_type()
    if query_type is not None:
        for key, value in query_type.fields.items():
            value.resolver = create_sync_resolver(client)

    mutation_type = schema.get_mutation_type()
    if mutation_type is not None:
        for key, value in mutation_type.fields.items():
            value.resolver = sync_resolver

    subscription_type = schema.get_subscription_type()
    if subscription_type is not None:
        # Two things preventing us from proxying subscriptions:
        #  - [ ] gql.Client does not expose subscriptions over websockets
        #  - [ ] need ability to stick with datasub's own subscriptions
        raise NotImplementedError("Schema with subscription type.")

    # Add missing abstract resolvers (scalar, unions, interfaces, ...)
    for key, value in schema.get_type_map().items():
        if hasattr(value, 'resolve_type'):
            value.resolve_type = typename_resolver
        elif isinstance(value, graphql.GraphQLScalarType):
            value.serialize = lambda x: x
            value.parse_value = lambda x: x
            value.parse_literal = lambda x: x
        elif isinstance(value, graphql.GraphQLObjectType):
            if not value.name.startswith("__") and value not in (
                query_type, mutation_type, subscription_type
            ):
                for k, v in value.fields.items():
                    v.resolver = default_merged_resolver
        elif hasattr(value, 'resolver'):
            raise NotImplementedError(
                "Missing resolver replacement for %s: %s." % (key, value)
            )

    return schema
