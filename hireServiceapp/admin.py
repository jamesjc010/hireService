from django.contrib import admin

# Register your models here.
from hireServiceapp.models import Seller, Customer, Driver

admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Driver)
