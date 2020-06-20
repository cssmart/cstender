from django.urls import path
from app.views import dump_report_view, dump_report_data, dump_download_report_parameter, download_dump_report,\
    mrn_status_report_parameter, mrn_status_report_view, mrn_status_report_gst_parameter,download_mrn_status_report,\
    mrn_report_download_parameter, mrn_status_report_gst_new_view, contribution_report_parameter,\
    contribution_get_report_data,contribution_report_download_parameter, download_contribution_report,\
    download_customer_ledger_passbook,DemoBootstrap3,data_save, download_customer_ledger_passbook,Form2Bootstrap3
from app.popups import customer_data
# from app.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('c_data/',customer_data, name='c_data'),
    path('customer_ledger_passbook', login_required(DemoBootstrap3.as_view())),
    path('clp/<str:p_org_id>/<str:p_cus_id>/', login_required(Form2Bootstrap3.as_view()), name='clp'),
    path('data_save',data_save, name='data_save'),
    path('clp_report', download_customer_ledger_passbook, name='customer_ledger_b_download'),

    path('dump_report', dump_report_view),
    path('mrn_form', mrn_status_report_parameter),
    path('contribution_form', contribution_report_parameter),
    path('mrn_gst_param', mrn_status_report_gst_parameter),
    path('sales_rtrn_download_param', dump_download_report_parameter),
    path('mrn_download_param', mrn_report_download_parameter),

    path('contribution_download_param', contribution_report_download_parameter),
    path('report', dump_report_data, name='dump'),
    path('mrn_report_view', mrn_status_report_view, name='mrn_report'),
    path('contribution_data', contribution_get_report_data, name='contribution_data'),
    path('mrn_gst_report', mrn_status_report_gst_new_view, name='mrn_gst_report'),
    path('report_download', download_dump_report, name='download'),
    path('report_mrn_download', download_mrn_status_report, name='report_download_mrn'),
    path('report_contribution_download', download_contribution_report, name='report_contribution_download'),
]
