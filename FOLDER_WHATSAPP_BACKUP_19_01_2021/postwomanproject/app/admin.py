from django.contrib import admin
from .models import SESSION_WINDOW,PALETTE_TABLE,PALETTE_STRUCTURE,INTERACTION_OUT,FUNCTION,\
    WHATSAPP_MAIL,INTERACTION_IN_TABLE,Mobile_No
# Register your models here.
admin.site.register(SESSION_WINDOW)
admin.site.register(PALETTE_STRUCTURE)
admin.site.register(PALETTE_TABLE)
admin.site.register(FUNCTION)
admin.site.register(INTERACTION_OUT)
admin.site.register(WHATSAPP_MAIL)
admin.site.register(INTERACTION_IN_TABLE)
admin.site.register(Mobile_No)
