from sanic import Sanic
from sanic_graphql import GraphQLView
from graphql_ws.websockets_lib import WsLibSubscriptionServer

import datasub.monitoring.e2e


def create(schema):

    app = Sanic()

    @app.middleware('request')
    async def setup_e2e(request):
        await datasub.monitoring.e2e.enter(request)

    @app.middleware('response')
    async def teardown_e2e(request, response):
        await datasub.monitoring.e2e.leave(request, response)

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

    return app
