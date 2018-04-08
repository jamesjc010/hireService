"""hireService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from hireServiceapp import views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^seller/sign-in/$', auth_views.login,
        {'template_name': 'seller/sign_in.html'},
        name = 'seller-sign-in'),
    url(r'^seller/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'seller-sign-out'),
    url(r'^seller/sign-up', views.seller_sign_up,
        name = 'seller-sign-up'),
    url(r'^seller/$', views.seller_home, name = 'seller-home'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
