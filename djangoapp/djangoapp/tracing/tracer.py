import os
from jaeger_client import Config
from opentracing_instrumentation.client_hooks import install_all_patches


from django.conf import settings

def tracer():
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': settings.JAEGER_AGENT_LOGGING,
            'local_agent': {
                'reporting_host': settings.JAEGER_AGENT_HOST,
                'reporting_port': settings.JAEGER_AGENT_PORT,
            }
        },
        service_name=settings.JAEGER_SERVICE_NAME)
    install_all_patches()
    monkeypatch_psycopg2_register_type()
    return config.initialize_tracer()

# Idea from https://github.com/aws/aws-xray-sdk-python/issues/243#issuecomment-746690693
def monkeypatch_psycopg2_register_type():
    import psycopg2._json

    f = psycopg2._json.register_type

    def func(obj, conn_or_curs):
        from opentracing_instrumentation.client_hooks._dbapi2 import ContextManagerConnectionWrapper

        if type(conn_or_curs) == ContextManagerConnectionWrapper:
            conn_or_curs = conn_or_curs.__wrapped__
        return f(obj, conn_or_curs)

    psycopg2._json.register_type = func
