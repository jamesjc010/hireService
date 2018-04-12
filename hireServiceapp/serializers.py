from rest_framework import serializers

#\ allows to break the line in import
from hireServiceapp.models import Seller, \
    Item, \
    Customer, \
    Driver, \
    Order, \
    OrderDetails

class SellerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    #inside SellerSerializer it gonna call get_image function,
    #and for image will return absolute uri
    def get_image(self, seller):
        request = self.context.get('request')
        image_url = seller.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Seller
        fields = ("id", "name", "phone", "address", "image")

class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, item):
        request = self.context.get('request')
        image_url = item.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Item
        fields = ("id", "name", "short_description", "image", "price", "size")

# ORDER SERIALIZER
class OrderCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")

class OrderDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Driver
        fields = ("id", "name", "avatar", "phone", "address", "capacity", "total_capacity")

class OrderSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ("id", "name", "phone", "address")

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "price", "size")

class OrderDetailsSerializer(serializers.ModelSerializer):
    item = OrderItemSerializer

    class Meta:
        model = OrderDetails
        fields = ("id", "item", "quantity", "sub_total")

class OrderSerializer(serializers.ModelSerializer):
    customer = OrderCustomerSerializer()
    driver = OrderDriverSerializer()
    seller = OrderSellerSerializer()
    order_details = OrderDetailsSerializer(many = True)
    #Don't need to use OrderItemSerializer because we have item assigned in OrderDetailsSerializer
    status = serializers.ReadOnlyField(source = "get_status_display")

    #
    #
    #   SHOULD I ADD SIZE HERE????
    #
    #
    class Meta:
        model = Order
        fields = ("id", "customer", "seller", "driver", "order_details", "total", "status", "address")
