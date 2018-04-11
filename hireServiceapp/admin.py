from django.contrib import admin

# Register your models here.
from hireServiceapp.models import Seller, Customer, Driver, Item, Order, OrderDetails

admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderDetails)
