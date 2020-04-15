from django.contrib import admin
from .models import VisitorManagementForm, MobileRegistered, FrequentVisitors
# Register your models here.
admin.site.register(VisitorManagementForm)
admin.site.register(MobileRegistered)
admin.site.register(FrequentVisitors)
