from django_api.models import *
from django_api.app_settings import *

import datetime

def can_request(api_key):
    """
    Check to see if the provided API key has been used above its limit for the last hour.
    
    If django_api will be used in a high volume environment,
    you should probably add another layer around this method.
    redis would be perfect for this.
    """
    now = datetime.datetime.now()
    limit = now - datetime.timedelta(hours=1)
    calls = APIKeyUsage.objects.filter(key=api_key, when__gt=limit).count()
    if calls > API_REQUESTS_PER_HOUR:
        return False
    return True

def register_api_usage(api_method, api_key):
    """
    Simple function to register usage of the API on a key.
    
    If django_api will be used in a high volume environment,
    you should probably add another layer around this method.
    E.g. a key-value db like redis, or memcached.
    """
    usage = APIKeyUsage(method=api_method, key=api_key).save()
    return True