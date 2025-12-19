from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

class Size(models.Model):
    """Product size options"""
    name = models.CharField(max_length=20, unique=True, db_index=True)
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extended user profile information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to say'),
    ]
    
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('staff', 'Staff'),
    ]
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES, default='customer')
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"
    
class Customer(models.Model):
    """Customer information for orders and cart"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='customer')
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        indexes = [
            models.Index(fields=['email', 'name']),
        ]
    
    def __str__(self):
        return self.name if self.name else self.email or f"Customer {self.id}"
    
    
class Product(models.Model):
    """Product catalog with size variants"""
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'XXL'),
    ]

    name = models.CharField(max_length=200, null=True, blank=True, db_index=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['name', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_size_display() if self.size else 'No size'})"

    @property
    def imageURL(self):
        """Return image URL or empty string if no image"""
        try:
            url = self.image.url
        except (ValueError, AttributeError):
            url = ''
        return url

    def get_size_choices(self):
        """Return available size choices"""
        return self.SIZE_CHOICES
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0
class Order(models.Model):
    """Customer order - can have many order items"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_ordered']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        indexes = [
            models.Index(fields=['-date_ordered']),
            models.Index(fields=['complete', '-date_ordered']),
        ]
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.name if self.customer else 'Guest'}"
    
    @property
    def shipping(self):
        """Determine if order requires shipping (has physical products)"""
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if not item.product.digital:
                shipping = True
                break
        return shipping
    
    @property
    def get_cart_total(self):
        """Calculate total cart value"""
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        """Get total number of items in cart"""
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    """Individual item in an order with quantity"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_items')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        indexes = [
            models.Index(fields=['order', '-date_added']),
        ]
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else 'Deleted Product'}"
    
    @property
    def get_total(self):
        """Calculate total price for this order item"""
        if self.product:
            total = self.product.price * self.quantity
            return total
        return 0
    
class ShippingAddress(models.Model):
    """Shipping address for physical product orders"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name='addresses')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='shipping_address')
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, default='USA')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} {self.zipcode}"
    
    @property
    def full_address(self):
        """Return formatted full address"""
        return f"{self.address}, {self.city}, {self.state} {self.zipcode}, {self.country}"
    
    
    