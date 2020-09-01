from django.contrib import admin
from .models import UserTable,PROJECT,PROJECT_RESOURCES,PEOPLE,TASK,DOCUMENT,TEAM,\
    APPLICATION,NOTIFICATIONS,UserForm,APPROVAL_HIERARCHY,TASK_APPROVALS
# Register your models here.
admin.site.register(UserTable)
admin.site.register(UserForm)
admin.site.register(PROJECT)
admin.site.register(PROJECT_RESOURCES)
admin.site.register(PEOPLE)
admin.site.register(TASK)
admin.site.register(DOCUMENT)
admin.site.register(TEAM)
admin.site.register(NOTIFICATIONS)
admin.site.register(TASK_APPROVALS)
admin.site.register(APPROVAL_HIERARCHY)
admin.site.register(APPLICATION)
# admin.site.register(Day)
