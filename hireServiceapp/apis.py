import json

from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from oauth2_provider.models import AccessToken

from hireServiceapp.models import Seller, Item, Order, OrderDetails
from hireServiceapp.serializers import SellerSerializer, ItemSerializer, OrderSerializer

##############
# CUSTOMER
##############

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

##############
# SELLER
##############
def seller_order_notification(request, last_request_time):
    notification = Order.objects.filter(seller = request.user.seller,
        created_at__gt = last_request_time).count()
    #This is this seller_order_notification code in sql
    #select count(*) from Orders
    #where seller = request.user.seller AND created_at > last_request_time

    return JsonResponse({"notification": notification})

##############
# DRIVER
##############

def driver_get_ready_orders(request):
    orders = OrderSerializer(
        Order.objects.filter(status = Order.READY, driver = None).order_by("-id"),
        many = True
    ).data
    return JsonResponse({"orders": orders})

# Post request from ouside system, need to exempt csrf to allow
##driver to post request to pick up an order
@csrf_exempt
# POST
# params: access_token, order_id
def driver_pick_order(request):

    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get Driver (based on this token)
        driver = access_token.user.driver

        ############################################
        #   EDIT THIS - MAKE IT CAPACITY INSTEAD   #
        ############################################
        # Check if Driver can only pick up one order at the same time
        if Order.objects.filter(driver = driver).exclude(status = Order.DELIVERED):
            return JsonResponse({"status": "failed", "error": "You can only pick one order at the same time."})

        # Prevents two driver from getting same order
        try:
            order = Order.objects.get(
                id = request.POST["order_id"],
                driver = None,
                status = Order.READY
            )
            #assign the driver
            order.driver = driver
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({"status": "success"})

        except Order.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This order has been picked up by another."})

    return JsonResponse({})

# GET
# params: access_token
def driver_get_latest_order(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())
    # Get driver
    driver = access_token.user.driver
    # Get data in json
    order = OrderSerializer(
        Order.objects.filter(driver = driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"order": order})

# POST
# params access_token, order_id
@csrf_exempt #since its a post request
def driver_complete_order(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    # Get driver
    driver = access_token.user.driver

    # Get order and update
    ############################################
    #   EDIT THIS - ADD DELIVERED TIME HERE    #
    ############################################
    order = Order.objects.get(id = request.POST["order_id"], driver = driver)
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({"status": "success"})

# GET
# params: access_token
def driver_get_revenue(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    # Get driver
    driver = access_token.user.driver

    from datetime import timedelta

    revenue = {}
    today = timezone.now()
    #weekday function returns integer representing a weekday
    #i.e monday is 0, sunday is 6
    current_weekdays = [today + timedelta(days = i) for i in range (0 - today.weekday(), 7 - today.weekday())]

    #returns all orders of a driver having status delivered for a specific year,month,day
    for day in current_weekdays:
        orders = Order.objects.filter(
            driver = driver,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day,
        )

        # Sums up total revenue for each day
        # strftime return Tue for Tuesday etc
        revenue[day.strftime("%a")] = sum(order.total for order in orders)

    return JsonResponse({"revenue": revenue})
