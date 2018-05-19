import uuid
import functools
import hashlib
import json
import asyncio

from datasub.utils.aiocache import taskcache as context

def get_dsruuid():
    return context["ds_request_uuid"]


async def enter(request):
    dsruuid = str(uuid.uuid4())
    print("Setup for %s" % dsruuid)
    context["ds_request_uuid"] = dsruuid

    # Log some of this stuff.
    # authsha = hashlib.sha256(
    #     request.headers.get('Authorization', '').encode('utf8')
    # ).hexdigest()
    # hashody = hashlib.sha256(
    #     json.dumps(request.json, sort_keys=True).encode('utf8')
    # ).hexdigest()


async def leave(request, response):
    dsruuid = get_dsruuid()
    print("Record for %s" % dsruuid)
    response.headers["DS-Request-UUID"] = dsruuid


def loggql_async(document, result):
    return asyncio.ensure_future(
        loggql(document, result, get_dsruuid())
    )


async def loggql(document, result, dsruuid=None):
    if dsruuid is None:
        dsruuid = get_dsruuid()
    print("LogGQL for %s" % dsruuid)

    # Log some of this stuff.
    print(type(document), document)
    print(type(result), result)
