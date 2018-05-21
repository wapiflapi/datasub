import graphene

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphene_sqlalchemy.converter import convert_sqlalchemy_type, convert_column_to_string

from sqlalchemy_utils import UUIDType

from datasub.monitoring import models


# Not sure why this is needed while it's not for JSONType.
convert_sqlalchemy_type.register(UUIDType)(convert_column_to_string)


class Request(SQLAlchemyObjectType):
    class Meta:
        model = models.Request
        interfaces = (relay.Node, )


class Execution(SQLAlchemyObjectType):
    class Meta:
        model = models.Execution
        interfaces = (relay.Node, )


class Operation(SQLAlchemyObjectType):
    class Meta:
        model = models.Operation
        interfaces = (relay.Node, )


class Fragment(SQLAlchemyObjectType):
    class Meta:
        model = models.Fragment
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    request = graphene.Field(Request)
    all_requests = SQLAlchemyConnectionField(Request)
    all_executions = SQLAlchemyConnectionField(Execution)
    all_operations = SQLAlchemyConnectionField(Operation)
    all_fragments = SQLAlchemyConnectionField(Fragment)


schema = graphene.Schema(query=Query)
print(schema)
