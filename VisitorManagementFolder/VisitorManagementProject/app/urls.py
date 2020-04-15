from django.urls import path
from . import views

urlpatterns = [
    path('vms/', views.DemoBootstrap3.as_view(), name="demo_bootstrap_3"),
    path('fv/', views.FrequentVisitorsFormData.as_view(), name="fv"),
    path('fv/<int:pk>/y', views.frequent_visitor_meet_yes, name='yes'),
    path('fv/<int:pk>/n', views.frequent_visitor_meet_no, name='no'),
    path('vms/<int:pk>/y', views.visitor_meet_yes, name='yes'),
    path('vms/<int:pk>/n', views.visitor_meet_no, name='no'),
    path('visitor_list', views.all_visitors_list, name='visitor_list'),
    path('approved_visitor', views.approved_visitor, name='approved_visitor'),
    path('rejected_visitor', views.rejected_visitor, name='rejected_visitor'),
    path('test', views.test, name='test'),
    path('punch_in', views.punch_in_details, name='punch_in_details'),
    path('security_approve/<int:pk>', views.security_approve, name='security'),
]