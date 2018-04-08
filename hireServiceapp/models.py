from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller')
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    image = models.ImageField(upload_to='seller_image/', blank=False)

    #gives resturant name instead of object no. in dashboard
    def __str__(self):
        return self.name
