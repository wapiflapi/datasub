import uuid
import functools
import json
import asyncio
import logging
import datetime

from datasub.utils.aiocache import taskcache as context
from datasub.monitoring.database import scoped_session
from datasub.monitoring.models import Request, Execution

logger = logging.getLogger(__name__)


def get_dsruuid():
    return context["dsruuid"]


async def enter(request):
    dsruuid = uuid.uuid4()
    logger.debug("enter(%s)", dsruuid)
    context["dsruuid"] = dsruuid

    with scoped_session() as session:
        request = Request(id=dsruuid)
        session.add(request)


async def leave(request, response):
    dsruuid = get_dsruuid()
    logger.debug("leave(%s)", dsruuid)
    response.headers["DS-Request-UUID"] = dsruuid

    with scoped_session() as session:
        request = session.query(Request).get(dsruuid)
        request.ds = (datetime.datetime.utcnow() - request.dt).total_seconds()


async def loggql(dsruuid, document, variable_values, result, dt, ds):
    logger.debug("loggql(%s)", dsruuid)

    with scoped_session() as session:
        execution = Execution.from_document(
            document, request_id=dsruuid,
            variables=variable_values, dt=dt, ds=ds,
        )
        session.add(execution)


def loggql_async(*args, **kwargs):
    return asyncio.ensure_future(
        loggql(get_dsruuid(), *args, **kwargs)
    )
