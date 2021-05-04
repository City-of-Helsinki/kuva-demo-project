from health_check.backends import BaseHealthCheckBackend
from health_check.exceptions import HealthCheckException
from django.conf import settings
import requests

class EndpointHealthCheck(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = True

    def check_status(self):
        jeager_agent_url = f"http://{settings.JAEGER_AGENT_HOST}:{settings.JAEGER_AGENT_HTTP_PORT}"
        try:
            r = requests.get(jeager_agent_url, timeout=0.5)
            if (r.status_code != 200):
                raise HealthCheckException('Jaeger not reachable')
        except Exception as e:
            raise HealthCheckException(f"Request failed: {e}")


    def identifier(self):
        return self.__class__.__name__  # Display name on the endpoint.
