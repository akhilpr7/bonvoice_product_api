from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Category, Product, Rating, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class RatingInline(admin.StackedInline):
    model = Rating
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'dummyjson_id', 'title', 'price',
        'category', 'stock', 'brand'
    ]
    list_filter = ['category']
    search_fields = ['title', 'brand']
    inlines = [RatingInline, ProductImageInline]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'rate', 'reviews_count']