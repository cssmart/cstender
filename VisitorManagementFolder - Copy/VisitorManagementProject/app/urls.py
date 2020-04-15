from django.urls import path
from . import views

urlpatterns = [
    path('vms/', views.DemoBootstrap3.as_view(), name="demo_bootstrap_3"),
    path('vms/<int:pk>/y', views.visitor_meet_yes, name='yes'),
    path('vms/<int:pk>/n', views.visitor_meet_no, name='no'),
    path('visitor_list', views.all_visitors_list, name='visitor_list'),
    path('approved_visitor', views.approved_visitor, name='approved_visitor'),
    path('rejected_visitor', views.rejected_visitor, name='rejected_visitor'),
    path('test', views.test, name='test'),
    path('mail', views.sendmail, name='sendmail')
]