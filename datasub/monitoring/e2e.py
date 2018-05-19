import uuid

from datasub.utils.aiocache import taskcache as context


async def setup(request):
    dsrid = str(uuid.uuid4())
    print("Setup for %s" % dsrid)
    context["ds_request_uuid"] = dsrid


async def record(request, response):
    dsrid = context.get("ds_request_uuid", "ooooooops")
    print("Record for %s" % dsrid)
    response.headers["DS-Request-UUID"] = dsrid
