from django.db import models
from sha import sha
import datetime

from django_api.app_settings import *

HTTP_METHODS = (
    ('POST', 'HTTP POST'),
    ('GET', 'HTTP GET'),
)
API_VALUE_TYPES = (
    ('str', 'String'),
    ('int', 'Integer'),
)
RESPONSE_FORMATS = (
    ('XML', 'XML'),
    ('JSON', 'JSON'),
)

REQUIRED_CHOICES = (
    ('OPT', 'Optional'),
    ('REQ', 'Required'),
)

class APIParameter(models.Model):
    name = models.CharField(max_length=200)
    value = models.CharField(max_length=20, choices=API_VALUE_TYPES)
    description = models.CharField(blank=True, max_length=255)
    required = models.CharField(max_length=30, choices=REQUIRED_CHOICES)

    def __unicode__(self):
        return self.name
    
    def is_required(self):
        if self.required == 'REQ':
            return True
        return False


class APIMethod(models.Model):
    name = models.CharField(unique=True, max_length=255, help_text="Do not use spaces. Only lowercase characters.")
    http_method = models.CharField(max_length=4, choices=HTTP_METHODS)
    response_format = models.CharField(max_length=10, choices=RESPONSE_FORMATS)
    internal_url = models.CharField(max_length=255, help_text="The original URL for the internal API. We'll request this page silently from your users, and deliver the content back to them.")
    allowed_parameters = models.ManyToManyField(APIParameter, blank=True, null=True)
    description = models.TextField(blank=True, help_text="Write a small text to describe the API")
    active = models.BooleanField(default=True, help_text="Is the current API method active?")
    
    class Meta:
        unique_together = ('response_format', 'name')
    
    def __unicode__(self):
        return self.name
        
    def get_full_url(self):
        return "%s%s%s" % (EXTERNAL_API_DOMAIN, EXTERNAL_API_BASE_PATH, self.name)
    
    def required_parameters(self):
        return self.allowed_parameters.filter(required='REQ')
    
    def optional_parameters(self):
        return self.allowed_parameters.filter(required='OPT')
    
    @property
    def api_settings(self):
        return {
            'domain': EXTERNAL_API_DOMAIN,
            'base_path': EXTERNAL_API_BASE_PATH,
        }

class APIKey(models.Model):
    key = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField()
    active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.key)
    
    def save(self):
        now = datetime.datetime.now()
        if not self.created:
            self.created = now
        
        if not self.key:
            self.key = self.generate_key()
        super(APIKey, self).save()
            
            
    def generate_key(self):
        is_used = False
        key = sha(str(datetime.datetime.now())).hexdigest()
        try:
            is_used = APIKey.objects.get(key=key)
        except:
            return key
        if is_used:
            return self.generate_key()
    

class APIKeyUsage(models.Model):
    key = models.ForeignKey(APIKey)
    method = models.ForeignKey(APIMethod)
    when = models.DateTimeField(blank=True)
    
    def save(self):
        if not self.when:
            self.when = datetime.datetime.now()
        super(APIKeyUsage, self).save()
    
    def __unicode__(self):
        return self.key.key