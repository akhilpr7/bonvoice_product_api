import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte'
    )
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains'
    )
    category = django_filters.CharFilter(
        field_name='category__name', lookup_expr='iexact'
    )
    min_rating = django_filters.NumberFilter(
        field_name='rating__rate', lookup_expr='gte'
    )
    brand = django_filters.CharFilter(
        field_name='brand', lookup_expr='icontains'
    )

    class Meta:
        model = Product
        fields = [
            'title', 'category', 'brand',
            'min_price', 'max_price', 'min_rating'
        ]
