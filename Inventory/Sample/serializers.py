from rest_framework import serializers
from .models import Euser,Category,Supplier,Product,Inventory



class EuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Euser
        fields = ['first_name','last_name','gender','phone','email','password','age']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


