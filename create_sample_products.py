"""
Create Sample Products for Errday Sportswear
Run: python manage.py shell < create_sample_products.py
"""

from store.models import Size, Product, Customer
from django.contrib.auth.models import User
from decimal import Decimal

# Create sizes
sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
for size_name in sizes:
    Size.objects.get_or_create(name=size_name)

print("✅ Sizes created")

# Create sample products
products_data = [
    {
        'name': 'Performance Running Shorts',
        'price': Decimal('49.99'),
        'digital': False,
        'description': 'Lightweight, breathable shorts perfect for your morning run',
        'size': 'M',
        'stock': 50,
        'is_active': True
    },
    {
        'name': 'Premium Compression T-Shirt',
        'price': Decimal('65.00'),
        'digital': False,
        'description': 'High-quality compression fit for optimal performance',
        'size': 'L',
        'stock': 35,
        'is_active': True
    },
    {
        'name': 'Training Hoodie Pro',
        'price': Decimal('89.99'),
        'digital': False,
        'description': 'Premium hoodie with moisture-wicking technology',
        'size': 'XL',
        'stock': 25,
        'is_active': True
    },
    {
        'name': 'Athletic Joggers',
        'price': Decimal('75.50'),
        'digital': False,
        'description': 'Comfortable joggers with tapered fit',
        'size': 'M',
        'stock': 40,
        'is_active': True
    },
    {
        'name': 'Sport Tank Top',
        'price': Decimal('35.00'),
        'digital': False,
        'description': 'Breathable tank for intense workouts',
        'size': 'S',
        'stock': 60,
        'is_active': True
    },
    {
        'name': 'Premium Sports Jacket',
        'price': Decimal('129.99'),
        'digital': False,
        'description': 'Water-resistant jacket for all weather conditions',
        'size': 'L',
        'stock': 15,
       'is_active': True
    },
]

for product_data in products_data:
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        defaults=product_data
    )
    if created:
        print(f"✅ Created: {product.name}")
    else:
        print(f"ℹ️  Already exists: {product.name}")

print("\n🎉 Sample data creation complete!")
print(f"Total products: {Product.objects.count()}")
print(f"Active products: {Product.objects.filter(is_active=True).count()}")
