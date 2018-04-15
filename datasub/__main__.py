import click

import gql

from gql.transport.requests import RequestsHTTPTransport
from graphql_ws.websockets_lib import WsLibSubscriptionServer

from sanic import Sanic
from sanic_graphql import GraphQLView

from datasub.utils.remote import make_remote_executable_schema

@click.command()
@click.argument('remote', envvar='DATASUB_REMOTE')
@click.option('--remote-authorization', '-A',
              envvar='DATASUB_REMOTE_AUTHORIZATION')
@click.option('--host', '-H', type=click.STRING, default='localhost',
              envvar='DATASUB_HOST', help='Datasub server hostname.')
@click.option('--port', '-P', type=click.INT, default=8000,
              envvar='DATASUB_PORT', help='Datasub server port.')
@click.option('--debug/--no-debug', default=False, help='Debug mode.')
def main(remote, remote_authorization, host, port, debug=False):

    headers = {}
    if remote_authorization is not None:
        headers['Authorization'] = remote_authorization

    client = gql.Client(
        transport=RequestsHTTPTransport(
            url=remote,
            headers=headers,
            use_json=True,
        ),
        fetch_schema_from_transport=True,
    )

    schema = make_remote_executable_schema(client.schema, client)

    app = Sanic()

    subscription_server = WsLibSubscriptionServer(schema)

    @app.websocket('/subscriptions', subprotocols=['graphql-ws'])
    async def subscriptions(request, ws):
        await subscription_server.handle(ws)
        return ws

    app.add_route(
        GraphQLView.as_view(schema=schema, graphiql=True), '/graphql'
    )

    app.add_route(
        GraphQLView.as_view(schema=schema, batch=True), '/graphql/batch'
    )

    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
