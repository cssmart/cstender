from django.conf.urls import url
from . import views
from django.views import generic


urlpatterns = [
    url(r'^workflow/app/tender/board_form/(?P<pk>\d+)/$', views.add_board_detail, name='board'),
    url(r'^workflow/app/tender/module/(?P<pk>\d+)/$', views.module_form_view, name='module'),
    url(r'^workflow/app/tender/component/(?P<pk>\d+)/$', views.add_component_list, name='component_list'),
    url(r'^workflow/app/tender/component_form_data/(?P<pk>\d+)/$', views.component_form_view, name='component'),
]
















# urlpatterns = [

# url('', views.module_form_view, name='module_form'),
# url('', generic.TemplateView.as_view(template_name="app/app/module_form.html"), name="module_form"),
# url(r'^module/(?P<id>\d+)/foo/$',
#     RedirectView.as_view(pattern_name="app/app/module_form.html"),
#     name="app/app/add_module.html"),
# url(r'^module/(?P<id>\d+)/$', views.module_form_view, name="app/app/module_form.html"),
# url('', views.add_board_list, name='list_board'),
# url(r'^task/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
#     # url('', views.IndexView.as_view(), name='index'),
#     # url('<int:pk>/', views.DetailView.as_view(), name='detail'),
#     # url('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
#     # url('<int:question_id>/vote/', views.vote, name='vote'),
#     # url('', generic.TemplateView.as_view(template_name="app/app/board_form.html"), name="board"),
#     # url('', views.home, name='home'),
#     # url('', views.board_form_view, name='board'),
#     # url('<int:pk>/', views.board_form_view.as_view(), name='board'),
#     url('workflow/app/tender/board_form/', views.board_form_view, name='board'),
#     # url(r'/161/', views.board_form_view, name='board'),
#     # url(r'^$', views.board_form_view(url='/id/', permanent=False)),
#     # url('<int:id>/', views.board_form_view.as_view()),
# ]
from django.views.generic import RedirectView