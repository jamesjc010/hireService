import sys
import os
import django

sys.path.append('hireService')
os.environ['DJANGO_SETTINGS_MODULE'] = 'hireService.settings'
django.setup()

from hireServiceapp.models import Seller

# From now onwards start your script..
if __name__ == '__main__':
    seller = Seller.objects.all()
    for s in seller:
        print(s.name)
