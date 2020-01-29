from django.urls import path,include
from .views import erp_view, sales_return_report

urlpatterns = [
    path('erp', erp_view),
    path('sales_report', sales_return_report, name='sales'),
]