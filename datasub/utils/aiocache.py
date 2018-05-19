import asyncio


class TaskCache():

    @property
    def cache(self):
        loop = asyncio.get_event_loop()
        try:
            return asyncio.Task.current_task(loop=loop)._datasub
        except AttributeError:
            asyncio.Task.current_task(loop=loop)._datasub = {}
            return asyncio.Task.current_task(loop=loop)._datasub

    def __getitem__(self, key):
        return self.cache[key]

    def __setitem__(self, key, value):
        self.cache[key] = value

    def __delitem__(self, key):
        del self.cache[key]

    def __contains__(self, key):
        return key in self.cache

    def __getattr__(self, name):
        return getattr(self.cache, name)


taskcache = TaskCache()
