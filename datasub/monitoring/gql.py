import gql

import datasub.monitoring.e2e


class Client(gql.Client):
    def execute(self, document, *args, **kwargs):
        result = super().execute(document, *args, **kwargs)
        datasub.monitoring.e2e.loggql_async(document, result)
        return result
