"""djangoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse, JsonResponse
from django.urls import path
import requests

urlpatterns = [
    path('admin/', admin.site.urls),
]

#
# Example view to show tracing of requests
#
def pr_view(*args, **kwargs):
  # Fetch a list of pull requests on the opentracing repository
  github_url = "https://api.github.com/repos/opentracing/opentracing-python/pulls"
  r = requests.get(github_url)

  json = r.json()
  pull_request_titles = map(lambda item: item['title'], json)

  return HttpResponse('OpenTracing Pull Requests: ' + ', '.join(pull_request_titles), status="200")

def users(*args, **kwargs):
    from django.contrib.auth.models import User, Group
    from django.contrib.sessions.models import Session
    from django.core import serializers
    serializers.serialize('json', User.objects.all())
    serializers.serialize('json', Group.objects.all())
    serializers.serialize('json', Session.objects.all())
    return HttpResponse("Made db calls for users, groups and sessions", status="200")
#
# Kubernetes liveness & readiness probes
#
def healthz(*args, **kwargs):
    return HttpResponse(status=200)


def readiness(*args, **kwargs):
    return HttpResponse(status=200)


urlpatterns += [path("healthz", healthz), path("readiness", readiness), path("pr", pr_view), path("users", users)]
