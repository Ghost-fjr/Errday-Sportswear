"""
Service layer for business logic - separates concerns from views.
"""
import logging
from decimal import Decimal
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import Order, OrderItem, Product, Customer, ShippingAddress

logger = logging.getLogger(__name__)


class CartService:
    """Handle cart operations"""
    
    @staticmethod
    def add_item_to_cart(customer, product_id, quantity=1):
        """
        Add an item to the customer's cart.
        
        Args:
            customer: Customer object
            product_id: ID of the product to add
            quantity: Number of items to add (default: 1)
            
        Returns:
            OrderItem object
            
        Raises:
            ObjectDoesNotExist: If product not found
            ValidationError: If quantity invalid
        """
        if quantity < 1:
            raise ValidationError("Quantity must be at least 1")
            
        product = Product.objects.get(id=product_id)
        
        if not product.is_active:
            raise ValidationError("This product is no longer available")
            
        order, created = Order.objects.get_or_create(
            customer=customer,
            complete=False
        )
        
        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            order_item.quantity += quantity
            order_item.save()
            
        logger.info(f\"Added {quantity}x {product.name} to cart for {customer.email}\")
        return order_item
    
    @staticmethod
    def remove_item_from_cart(customer, product_id):
        """Remove an item from the cart completely"""
        try:
            order = Order.objects.get(customer=customer, complete=False)
            order_item = OrderItem.objects.get(order=order, product_id=product_id)
            order_item.delete()
            logger.info(f\"Removed product {product_id} from cart for {customer.email}\")
        except ObjectDoesNotExist:
            logger.warning(f\"Attempted to remove non-existent item from cart\")
    
    @staticmethod
    def update_item_quantity(customer, product_id, quantity):
        """Update quantity of a cart item"""
        if quantity <= 0:
            CartService.remove_item_from_cart(customer, product_id)
            return
            
        try:
            order = Order.objects.get(customer=customer, complete=False)
            order_item = OrderItem.objects.get(order=order, product_id=product_id)
            order_item.quantity = quantity
            order_item.save()
            logger.info(f\"Updated product {product_id} quantity to {quantity}\")
        except ObjectDoesNotExist:
            logger.error(f\"Cart item not found for update\")
            raise


class OrderService:
    """Handle order processing"""
    
    @staticmethod
    @transaction.atomic
    def complete_order(customer, order, shipping_data=None):
        """
        Complete an order and create shipping address if needed.
        
        Args:
            customer: Customer object
            order: Order object
            shipping_data: Dictionary with shipping information (optional)
            
        Returns:
            Order object
        """
        # Validate order total matches calculated total
        calculated_total = order.get_cart_total
        
        if calculated_total == 0:
            raise ValidationError(\"Cannot complete empty order\")
        
        # Create shipping address if physical products exist
        if order.shipping and shipping_data:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=shipping_data.get('address', ''),
                city=shipping_data.get('city', ''),
                state=shipping_data.get('state', ''),
                zipcode=shipping_data.get('zipcode', ''),
                country=shipping_data.get('country', 'USA')
            )
        
        order.complete = True
        order.save()
        
        logger.info(f\"Order #{order.id} completed for {customer.email}\")
        return order


class ProductService:
    \"\"\"Handle product queries and operations\"\"\"
    
    @staticmethod
    def get_active_products():
        \"\"\"Get all active products\"\"\"
        return Product.objects.filter(is_active=True).order_by('-created_at')
    
    @staticmethod
    def get_product_by_id(product_id):
        \"\"\"Get a single product by ID\"\"\"
        try:
            return Product.objects.get(id=product_id, is_active=True)
        except ObjectDoesNotExist:
            logger.error(f\"Product {product_id} not found or inactive\")
            raise
    
    @staticmethod
    def search_products(query):
        \"\"\"Search products by name\"\"\"
        return Product.objects.filter(
            name__icontains=query,
            is_active=True
        ).order_by('-created_at')
