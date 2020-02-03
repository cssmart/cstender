from django.urls import path,include
from .views import dump_report_view, dump_report_data

urlpatterns = [
    path('dump_report', dump_report_view),
    path('report', dump_report_data, name='dump'),

]