from django.http import *
from django.template import Context, RequestContext, loader



def render(request, template, v=None):
    if v == None:
        v = {}
    t = loader.get_template(template)
    c = RequestContext(request, v)
    return HttpResponse(t.render(c))