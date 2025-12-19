"""
Update existing products with actual images and create categories
Run: python manage.py shell < update_products_images.py
"""

from store.models import Product

# Map products to images
product_images = {
    'Performance Running Shorts': 'men.jpeg',
    'Premium Compression T-Shirt': 'men_Cgv2qJB.jpeg',
    'Training Hoodie Pro': 'climate.jpeg',
    'Athletic Joggers': 'men_DSZxW4H.jpeg',
    'Sport Tank Top': 'women.jpeg',
    'Premium Sports Jacket': 'climate_1V7mMA5.jpeg',
}

# Update products with images
for product_name, image_name in product_images.items():
    try:
        product = Product.objects.get(name=product_name)
        product.image = f'products/{image_name}'
        product.save()
        print(f"✅ Updated {product_name} with image {image_name}")
    except Product.DoesNotExist:
        print(f"⚠️  Product not found: {product_name}")

# Add more products with images
new_products = [
    {
        'name': 'Women\'s Active Leggings',
        'price': 55.00,
        'digital': False,
        'description': 'High-waisted leggings with perfect stretch',
        'image': 'products/women_Gp2QI3y.jpeg',
        'size': 'M',
        'stock': 45,
        'is_active': True
    },
    {
        'name': 'Climate Control Jacket',
        'price': 145.00,
        'digital': False,
        'description': 'Advanced temperature regulation technology',
        'image': 'products/climate_3NYZzjd.jpeg',
        'size': 'L',
        'stock': 20,
        'is_active': True
    },
    {
        'name': 'Performance Training Set',
        'price': 95.00,
        'digital': False,
        'description': 'Complete training outfit for peak performance',
        'image': 'products/beautiful.webp',
        'size': 'L',
        'stock': 30,
        'is_active': True
    },
]

for product_data in new_products:
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults=product_data
    )
    if created:
        print(f"✅ Created: {product.name}")
    else:
        print(f"ℹ️  Already exists: {product.name}")

print("\n🎉 Products updated with images!")
print(f"Total products: {Product.objects.count()}")
