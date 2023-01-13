from rest_framework import serializers

from base import models


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

    def get_image(self, product):
        request = self.context.get('request')
        return request.build_absolute_uri(product.image_url)


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField('get_product')
    class Meta:
        model = models.OrderItem
        fields = ['quantity', 'get_total', 'product']

    def get_product(self, obj):
        prroduct = obj.product
        return ProductSerializer(instance=prroduct, context=self.context).data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ['get_cart_total', 'get_cart_items', 'date_ordered']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = '__all__'

