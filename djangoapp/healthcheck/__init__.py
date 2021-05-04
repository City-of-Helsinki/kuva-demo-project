from django.apps import AppConfig
from health_check.plugins import plugin_dir

class HealthCheckConfig(AppConfig):
    name = 'healthcheck'

    def ready(self):
        from .endpoint import EndpointHealthCheck
        plugin_dir.register(EndpointHealthCheck)

default_app_config = 'healthcheck.HealthCheckConfig'
