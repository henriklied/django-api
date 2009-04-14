from django.http import *
import simplejson

def HttpResponseKeyMissing():
    return HttpResponseForbidden(simplejson.dumps({'error': 'You must supply an API key via the api_key parameter'}), mimetype="application/json")

def HttpResponseNonValidAPIMethod():
    return HttpResponseNotFound(simplejson.dumps({'error': 'The API method you requested could not be found'}), mimetype="application/json")

def HttpResponseNonValidAPIKey():
    return HttpResponseNotFound(simplejson.dumps({'error': 'The API key you supplied was not found.'}), mimetype="application/json")

def HttpResponseWrongHttpMethod(used_method, required_method):
    return HttpResponseBadMethod(simplejson.dumps({'error': 'You called this API method via %s while the spec says it must be called via %s' % (used_method, required_method)}), mimetype="application/json")

def HttpResponseOverCallLimit():
    return HttpResponseForbidden(simplejson.dumps({'error': 'You have reached the maximum allowed API calls in an hour. Please wait a while.'}), mimetype="application/json")
    
def HttpResponseUnknownError():
    return HttpResponseServerError(simplejson.dumps({'error': 'An unknown error occured. The administrators have been notified.'}), mimetype="application/json")