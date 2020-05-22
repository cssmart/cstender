from django.contrib import admin
from .models import SESSION_WINDOW,PALETTES,PALETTE_STRUCTURE,INTERACTION_OUT,FUNCTION

# Register your models here.
admin.site.register(SESSION_WINDOW)
admin.site.register(PALETTE_STRUCTURE)
admin.site.register(PALETTES)
admin.site.register(FUNCTION)
admin.site.register(INTERACTION_OUT)