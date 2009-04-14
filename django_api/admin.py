from django.contrib import admin
from django_api.models import *

class APIParameterAdmin(admin.ModelAdmin):
    pass
    

class APIMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'http_method', 'internal_url', 'response_format', 'active')
    list_filter = ('http_method', 'response_format', 'active')    
    ordering = ['-name',]
    filter_horizontal = ('allowed_parameters',)    
    search_fields = ('name', 'description')


class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'active',)
    list_filter = ('active',)    
    ordering = ['-key',]
    search_fields = ('key', )


class APIKeyUsageAdmin(admin.ModelAdmin):
    pass


admin.site.register(APIParameter, APIParameterAdmin)
admin.site.register(APIMethod, APIMethodAdmin)
admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(APIKeyUsage, APIKeyUsageAdmin)