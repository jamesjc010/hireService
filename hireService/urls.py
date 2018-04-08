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
from django.conf.urls import url, include
from django.contrib import admin
from hireServiceapp import views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),

    # Seller
    url(r'^seller/sign-in/$', auth_views.login,
        {'template_name': 'seller/sign_in.html'},
        name = 'seller-sign-in'),
    url(r'^seller/sign-out', auth_views.logout,
        {'next_page': '/'},
        name = 'seller-sign-out'),
    url(r'^seller/sign-up', views.seller_sign_up,
        name = 'seller-sign-up'),
    url(r'^seller/$', views.seller_home, name = 'seller-home'),

    url(r'^seller/account/$', views.seller_account, name = 'seller-account'),
    url(r'^seller/item/$', views.seller_item, name = 'seller-item'),
    url(r'^seller/order/$', views.seller_order, name = 'seller-order'),
    url(r'^seller/report/$', views.seller_report, name = 'seller-report'),

    # Sign In/ Sign Out/ Sign Up
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign-in/ sign_up)
    # /revoke-token (sign-out)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
