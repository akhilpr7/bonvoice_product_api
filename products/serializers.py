from rest_framework import serializers
from .models import Category, Product, Rating, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'product_count']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rate', 'reviews_count']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'url', 'order']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'dummyjson_id', 'title', 'price',
            'discount_percentage', 'stock', 'brand',
            'thumbnail', 'category', 'category_name',
            'rating', 'created_at',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    rating = RatingSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'dummyjson_id', 'title', 'description',
            'price', 'discount_percentage', 'stock', 'brand',
            'thumbnail', 'images', 'category', 'category_name',
            'rating', 'created_at', 'updated_at',
        ]