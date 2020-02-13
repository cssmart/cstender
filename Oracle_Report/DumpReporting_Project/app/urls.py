from django.urls import path
# from .views import dump_report_view, dump_report_data, dump_download_report_parameter, download_dump_report,\
#     mrn_status_report_parameter, mrn_status_report_view
from app.views import *

urlpatterns = [
    path('dump_report', dump_report_view),
    path('mrn_report', mrn_status_report_parameter),
    path('sales_rtrn_download_param', dump_download_report_parameter),
    path('mrn_download_param', mrn_report_download_parameter),
    path('report', dump_report_data, name='dump'),
    path('mrn_report_view', mrn_status_report_view, name='mrn_report'),
    path('report_download', download_dump_report, name='download'),
    path('report_mrn_download', download_mrn_status_report, name='report_download_mrn'),
]
