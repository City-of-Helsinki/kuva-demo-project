import os
import django_opentracing
from jaeger_client import Config
from opentracing_instrumentation.client_hooks import requests, urllib, urllib2

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
    # Have to do 1 by 1, as psycopg2 instrumentation is not working with Django
    requests.install_patches()
    urllib.install_patches()
    urllib2.install_patches()
    return config.initialize_tracer()
