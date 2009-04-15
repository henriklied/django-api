from django.http import *

import httplib, urllib, uri

from django_api.models import *
from django_api.utils.http_methods import *
from django_api.utils.etc import *
from django_api.utils import render
from django_api.app_settings import *



def api_request(request, api_name):
    """
    This view requires the 'api_name' parameter
    as well as one hardcoded required request.REQUEST parameter, 'api_key'
    """
    
    # Check if the user has supplied us with an API key
    if not 'api_key' in request.REQUEST:
        return HttpResponseKeyMissing()
    
    # Check that the supplied API key is in the registry.
    # This should probably be a list in memcached, for performance sake
    try:
        api_key = APIKey.objects.get(key=request.REQUEST.get('api_key'), active=True)
    except:
        return HttpResponseNonValidAPIKey()
    
    # Get the number of requests made by the API key
    # and check if the user is above his/her limit.
    if not can_request(api_key):
        return HttpResponseOverCallLimit()
    
    # Check that the api_name parameter actually exists
    try:
        api_method = APIMethod.objects.get(name=api_name, active=True)
    except:
        return HttpResponseNonValidAPIMethod()
    
    # Check that the required API method matches the one in the request.
    if request.method != api_method.http_method:
        return HttpResponseWrongHttpMethod(request.method, api_method.http_method)
    
    
    params = getattr(request, api_method.http_method)
    #assert False
    
    internal_url = api_method.internal_url
    
    
    # Check that the request has all the required api parameters.
    if not set(params.__dict__) >= set([param.name for param in api_method.required_parameters()]):
        return HttpResponse('To complete this API call, you must provide the following parameter(s): %s' % ", ".join([param.name for param in api_method.required_parameters()]))
        
    # Connect to the internal api domain / ip
    # 
    # (If there's only one, you can move the line below outside the function.)
    connection = httplib.HTTPConnection(INTERNAL_API_DOMAIN)
    
    # httplib needs the params in the body when POSTing, and in the URL white GETing
    if request.method == 'POST':
        connection.request(request.method, '%s%s' % (INTERNAL_API_BASE_PATH, internal_url), urllib.urlencode(params))
    else:
        connection.request(request.method, '%s%s?%s' % (INTERNAL_API_BASE_PATH, internal_url, urllib.urlencode(params)))
    response = connection.getresponse()
    
    response_data = response.read()
    
    # It's important that your underlying API returns proper status codes.
    # If the API call doesn't return HTTP 200, the user is given an error.
    # 
    # An email is sent to the admins with the error.
    #
    
   
    # This function inserts an API hit into the database.
    # It should be called right before we deliver the content back to the user.
    register_api_usage(api_method, api_key)
    return HttpResponse(response_data)


def api_doc(request):
    """
    Returns the generated API documentation using all active API methods.
    """
    api_methods = APIMethod.objects.filter(active=True)
    return render(request, 'django_api/api_doc.html', 
        {'api_methods': api_methods}
    )