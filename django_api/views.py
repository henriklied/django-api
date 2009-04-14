from django.http import *

import httplib, urllib

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
    
    
    params = urllib.urlencode(request.REQUEST.__dict__)
    
    # Connect to the internal api domain / ip
    # 
    # (If there's only one, you can move the line below outside the function.)
    connection = httplib.HTTPConnection(INTERNAL_API_DOMAIN)
    connection.request(request.method, '%s%s' % (INTERNAL_API_BASE_PATH, api_method.internal_url), params)
    response = connection.getresponse()
    
    response_data = response.read()
    
    # It's important that your underlying API returns proper status codes.
    # If the API call doesn't return HTTP 200, the user is given an error.
    # 
    # An email is sent to the admins with the error.
    #
    if response.status != 200:
        from django.core.mail import mail_admins
        message = """
        An error occured when trying to fetch %s%s%s.
        Internal API HTTP status code: HTTP %d
        
        Internal API response:
        %s
        """ % (INTERNAL_API_DOMAIN, INTERNAL_API_BASE_PATH, api_method.internal_url, response.status, response_data)
        mail_admins('Error in API call', message)
        return HttpResponseUnknownError()
    
    # This function inserts an API hit into the database.
    # It should be called right before we deliver the content back to the user.
    register_api_usage(api_method, api_key)
    return HttpResponse(response_data)


def api_doc(request):
    api_methods = APIMethod.objects.filter()
    return render(request, 'django_api/api_doc.html', 
        {'api_methods': api_methods}
    )