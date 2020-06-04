"""ApexSOA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
from POC_APP import views as PO_VIEW
from loginmodule.views import login, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    # POC urls=======================================================================================
    path('POC/',PO_VIEW.POC_view),
    path('detailpo/<int:pid>/', PO_VIEW.POC_MORE_DETAIL_INFO, name='poc_detail'),
    # ApexSoaItems urls==============================================================================
    path('ApexSoaItemsData/', views.apex_soa_view),
    path('ApexSoaItems/',views.apex_soa_view_demo),
    path('<str:pk>/n', views.reject_item, name='no'),
    path('<str:id>/<str:id1>/<str:id2>/<str:id3>/<int:id4>/y', views.approved_yes, name='yes'),
    # Login===========================================================================================
    path('<int:pk>', login, name='poc'),
    path('logout/', logout),
    path('loginmodule/', include('loginmodule.urls')),
]


import execute