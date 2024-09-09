from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'content', 'image', 'category', 'tags', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
