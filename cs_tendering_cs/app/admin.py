from django.contrib import admin
from .models import TenderDataProcess,TenderDataDetails, BodyDetails, BoardDetails, ModuleDetails, ComponentDetails,TEM, BOARDS
# Register your models here.
admin.site.register(TenderDataProcess)
admin.site.register(TenderDataDetails)
admin.site.register(BodyDetails)
admin.site.register(ModuleDetails)
admin.site.register(BoardDetails)
admin.site.register(ComponentDetails)
admin.site.register(TEM)
admin.site.register(BOARDS)
