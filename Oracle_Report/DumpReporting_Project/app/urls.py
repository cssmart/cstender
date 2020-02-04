from django.urls import path,include
from .views import dump_report_view, dump_report_data, dump_download_report_parameter, download_dump_report

urlpatterns = [
    path('dump_report', dump_report_view),
    path('download_report', dump_download_report_parameter),
    path('report', dump_report_data, name='dump'),
    path('report_download', download_dump_report, name='download'),

]
