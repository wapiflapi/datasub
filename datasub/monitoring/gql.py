import datetime

import gql

import datasub.monitoring.e2e


class Client(gql.Client):
    def execute(self, document, variable_values, **kwargs):
        dt = datetime.datetime.utcnow()
        result = super().execute(document, variable_values, **kwargs)
        ds = (datetime.datetime.utcnow() - dt).total_seconds()
        datasub.monitoring.e2e.loggql_async(document, variable_values, result, dt, ds)
        return result
