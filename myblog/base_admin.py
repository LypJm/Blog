
from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super(BaseAdmin, self).get_queryset(request).filter(owner=request.user)
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseAdmin, self).save_model(request, obj, form, change)