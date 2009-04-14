from django.conf import settings

INTERNAL_API_DOMAIN = getattr(settings, 'INTERNAL_API_DOMAIN', 'localhost:9000')
INTERNAL_API_BASE_PATH = getattr(settings, 'INTERNAL_API_DOMAIN', '/api/')
API_REQUESTS_PER_HOUR = getattr(settings, 'API_REQUESTS_PER_HOUR', 120)

EXTERNAL_API_DOMAIN = getattr(settings, 'EXTERNAL_API_DOMAIN', 'localhost:8000')
EXTERNAL_API_BASE_PATH = getattr(settings, 'INTERNAL_API_DOMAIN', '/api/')
