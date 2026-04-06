from django.shortcuts import render

# Create your views here.
import json
from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Min, Max

from .models import Product, Category
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    CategorySerializer,
)
from .filters import ProductFilter
from .services import fetch_and_sync_products


class ProductViewSet(viewsets.ModelViewSet):
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'brand']
    # ordering_fields = ['price', 'rating__rate', 'stock', 'created_at']
    ordering = ['dummyjson_id']

    def get_queryset(self):
        return (
            Product.objects
            .select_related('category', 'rating')
            .prefetch_related('images')
            .all()
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    def list(self, request, *args, **kwargs):

        #List products — check Redis cache first.

        cache_key = f"products:list:{request.query_params.urlencode()}"
        cached = cache.get(cache_key)

        if cached:
            return Response(cached)

        response = super().list(request, *args, **kwargs)


        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)

        return response

    def retrieve(self, request, *args, **kwargs):

        pk = kwargs.get('pk')
        cache_key = f"products:detail:{pk}"
        cached = cache.get(cache_key)

        if cached:
            return Response(cached)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)
        return response

    @action(detail=False, methods=['post'])
    def sync(self, request):

        try:
            created, updated = fetch_and_sync_products()

            # Clear all product cache after sync
            cache.delete_pattern("products:*")

            return Response({
                'message': 'Sync successful',
                'created': created,
                'updated': updated,
                'total': created + updated,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )


    @action(detail=False, methods=['get'])
    def categories(self, request):
   
        cache_key = "products:categories"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        categories = Category.objects.annotate(
            product_count=Count('products')
        ).order_by('name')
        serializer = CategorySerializer(categories, many=True)

        cache.set(cache_key, serializer.data, timeout=settings.CACHE_TTL)
        return Response(serializer.data)