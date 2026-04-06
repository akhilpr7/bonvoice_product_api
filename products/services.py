import requests
from django.conf import settings
from django.utils.text import slugify
from .models import Category, Product, Rating, ProductImage


def fetch_and_sync_products():

    try:
        response = requests.get(
            f"{settings.DUMMYJSON_URL}/products",
            params={'limit': 100},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise Exception(f"DummyJSON API error: {str(e)}")

    products_data = data.get('products', [])
    created = 0
    updated = 0

    for item in products_data:
        cat_name = item.get('category', 'uncategorized')
        category, _ = Category.objects.get_or_create(
            name=cat_name,
            defaults={'slug': slugify(cat_name)}
        )

        product, is_created = Product.objects.update_or_create(
            dummyjson_id=item['id'],
            defaults={
                'title': item.get('title', ''),
                'description': item.get('description', ''),
                'price': item.get('price', 0),
                'discount_percentage': item.get('discountPercentage', 0),
                'stock': item.get('stock', 0),
                'brand': item.get('brand', ''),
                'thumbnail': item.get('thumbnail', ''),
                'category': category,
            }
        )

        Rating.objects.update_or_create(
            product=product,
            defaults={
                'rate': item.get('rating', 0),
                'reviews_count': len(item.get('reviews', [])),
            }
        )

        images = item.get('images', [])
        if images and is_created:
            ProductImage.objects.bulk_create([
                ProductImage(product=product, url=url, order=i)
                for i, url in enumerate(images)
            ])

        if is_created:
            created += 1
        else:
            updated += 1

    return created, updated