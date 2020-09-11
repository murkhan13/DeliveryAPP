"""cronProjectAPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf.urls.static import static
from cronProjectAPI import settings
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/catalog/', include('catalog.urls')),
    #For logins
    re_path(r'^api/v1/', include('accounts.urls')),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/', include('orders.urls')),
    path('api/v1/', include('feedbacks.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)