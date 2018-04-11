from rest_framework import serializers

from hireServiceapp.models import Seller

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
