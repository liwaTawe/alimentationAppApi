from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerialiser(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemsSerializer(serializers.ModelSerializer):
    cart = CartSerializer
    products = ProductSerialiser
    cart = CartSerializer()
  
    class Meta:
        model = CartItems
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'