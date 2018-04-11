from django.http import JsonResponse

from hireServiceapp.models import Seller
from hireServiceapp.serializers import SellerSerializer

#here we call api functions, whenever we run api function we call this function
#this function name is for customer
#returns all resturants in db in json data
def customer_get_sellers(request):
    sellers = SellerSerializer(
        Seller.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"sellers": sellers})
