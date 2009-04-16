from django.http import *
from django.template import Context, RequestContext, loader

from django_api import app_settings as settings


def render(request, template, v=None):
    if v == None:
        v = {}
    v['settings'] = settings
    t = loader.get_template(template)
    c = RequestContext(request, v)
    return HttpResponse(t.render(c))