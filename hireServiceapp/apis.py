import json

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.models import AccessToken

from hireServiceapp.models import Seller, Item, Order, OrderDetails
from hireServiceapp.serializers import SellerSerializer, ItemSerializer, OrderSerializer

# We call api functions here, whenever we run api function we call this function
## this function name is for customer
## returns all resturants in db in json data
def customer_get_sellers(request):
    sellers = SellerSerializer(
        Seller.objects.all().order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"sellers": sellers})

def customer_get_items(request, seller_id):
    items = ItemSerializer(
        Item.objects.filter(seller_id = seller_id).order_by("-id"),
        many = True,
        context = {"request": request}
    ).data

    return JsonResponse({"items": items})

@csrf_exempt
def customer_add_order(request):
    # This is a block comment. (i.e. a comment)
    ## This function requires (illict?/explict?) parameters
    """
        params:
            access_token
            seller_id
            address
            order_details (json format), example:
                [{"item_id": 1, "quantity": 2},{"item_id": 2, "quantity": 3}]
            stripe_token

            return:
                {"status": "success"}
    """

    if request.method == "POST":
        # Get token from parameters
        # expires__gt means expires greater than today i.e. make sure the token isnt expired yet
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get Profile
        ## can get customer from user in access_token (as you see in django dashboard)
        customer = access_token.user.customer

        # Check whether customer has any order that is not delivered
        # current order must be completed before new order can be placed
        if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "fail", "error": "Your last order must be completed."})

        # Check Address
        # If user doesnt provide address or address is null
        if not request.POST["address"]:
            return JsonResponse({"status": "fail", "error": "Address is required."})

        # Get Order Details
        ## Load it into json format
        order_details = json.loads(request.POST["order_details"])

        # calculate total amount (sub_total) of order (i.e. might have multiple order details)
        order_total = 0
        for item in order_details:
            order_total += Item.objects.get(id = item["item_id"]).price * item["quantity"]

        # calculate total size of order (i.e. might have multiple order details)
        total_size = 0
        for item in order_details:
            total_size += Item.objects.get(id = item["item_id"]).size * item["quantity"]

        ## if length of order details (i.e. how many order_details) is greater than zero
        if len(order_details) > 0:
            # Step 1 - Create Order
            order = Order.objects.create(
                customer = customer,
                seller_id = request.POST["seller_id"],
                total = order_total,
                total_size = total_size,
                status = Order.PREPARING,
                address = request.POST["address"]
            )

            # Step 2 - Create Order Details
            for item in order_details:
                OrderDetails.objects.create(
                    order = order,
                    item_id = item["item_id"],
                    quantity = item["quantity"],
                    sub_total = Item.objects.get(id = item["item_id"]).price * item["quantity"]
                )

            return JsonResponse({"status": "success"})


def customer_get_latest_order(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    # this gets last order of customer from database
    customer = access_token.user.customer
    order = OrderSerializer(Order.objects.filter(customer = customer).last()).data

    return JsonResponse({"order": order})

def seller_order_notification(request, last_request_time):
    notification = Order.objects.filter(seller = request.user.seller,
        created_at__gt = last_request_time).count()
    #This is this seller_order_notification code in sql
    #select count(*) from Orders
    #where seller = request.user.seller AND created_at > last_request_time

    return JsonResponse({"notification": notification})
