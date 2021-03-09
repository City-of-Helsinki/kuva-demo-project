from django.conf import settings
from django.db import connection
from django_opentracing import OpenTracingMiddleware

class IgnoreTracingMiddleware(OpenTracingMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # determine whether this middleware should be applied
        # NOTE: if tracing is on but not tracing all requests, then the tracing
        # occurs through decorator functions rather than middleware

        ignored_paths = getattr(settings, 'OPENTRACING_TRACE_IGNORED', [])

        if not self._tracing._trace_all or request.path in ignored_paths:
            return None

        if hasattr(settings, 'OPENTRACING_TRACED_ATTRIBUTES'):
            traced_attributes = getattr(settings,
                                        'OPENTRACING_TRACED_ATTRIBUTES')
        else:
            traced_attributes = []
        self._tracing._apply_tracing(request, view_func, traced_attributes)
