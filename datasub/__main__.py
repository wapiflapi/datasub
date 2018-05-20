import asyncio
import logging

import click

from gql.transport.requests import RequestsHTTPTransport

import datasub.monitoring.gql
import datasub.app

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
@click.option('--reset-db/--no-reset-db', default=False, help='Reset database.')
def main(remote, remote_authorization, host, port, debug=False, reset_db=False):

    if debug:
        logging.basicConfig(level=logging.DEBUG)

    if reset_db:
        from datasub.monitoring.database import engine
        from datasub.monitoring.models import Base
        Base.metadata.create_all(bind=engine)

    headers = {}
    if remote_authorization is not None:
        headers['Authorization'] = remote_authorization

    client = datasub.monitoring.gql.Client(
        transport=RequestsHTTPTransport(
            url=remote,
            headers=headers,
            use_json=True,
        ),
        fetch_schema_from_transport=True,
    )

    schema = make_remote_executable_schema(client.schema, client)

    app = datasub.app.create(schema)
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
