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
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from hireServiceapp import views, apis

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
    url(r'^seller/item/add/$', views.seller_add_item, name = 'seller-add-item'),
    # Note: \d+ refers to numbers, .+ means string
    url(r'^seller/item/edit/(?P<item_id>\d+)/$', views.seller_edit_item, name = 'seller-edit-item'),
    url(r'^seller/order/$', views.seller_order, name = 'seller-order'),
    url(r'^seller/report/$', views.seller_report, name = 'seller-report'),

    # Sign In/ Sign Out/ Sign Up
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign-in/ sign_up)
    # /revoke-token (sign-out)
    url(r'^api/seller/order/notification/(?P<last_request_time>.+)/$', apis.seller_order_notification),

    # APIs for CUSTOMERS
    #when someone calls this url it calls the customer_get_sellers function
    url(r'^api/customer/sellers/$', apis.customer_get_sellers),
    url(r'^api/customer/items/(?P<seller_id>\d+)/$', apis.customer_get_items),
    url(r'^api/customer/order/add/$', apis.customer_add_order),
    url(r'^api/customer/order/latest/$', apis.customer_get_latest_order),
    url(r'^api/customer/driver/location/$', apis.customer_driver_location),

    # APIs for DRIVERS
    url(r'^api/driver/orders/ready/$', apis.driver_get_ready_orders),
    url(r'^api/driver/orders/pick/$', apis.driver_pick_order),
    url(r'^api/driver/orders/latest/$', apis.driver_get_latest_order),
    url(r'^api/driver/orders/complete/$', apis.driver_complete_order),
    url(r'^api/driver/revenue/$', apis.driver_get_revenue),
    url(r'^api/driver/location/update/$', apis.driver_update_location),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
