import json
import logging
from .models import Product, Order, OrderItem, Customer
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

def cookieCart(request):
    """
    Retrieve and process cart data from cookies for anonymous users.
    
    Args:
        request: Django HTTP request object
        
    Returns:
        dict: Dictionary containing cart items, order summary, and items list
    """
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except (json.JSONDecodeError, TypeError) as e:
        logger.warning(f"Invalid cart cookie data: {e}")
        cart = {}
            
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False} 
    cartItems = order['get_cart_items']
            
    for product_id in cart:
        try:
            cartItems += cart[product_id].get("quantity", 0)
                    
            product = Product.objects.get(id=product_id)
            quantity = cart[product_id].get("quantity", 0)
            total = (product.price * quantity)
                    
            order['get_cart_total'] += total     
            order['get_cart_items'] += quantity
                    
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                    'size': product.size,
                },
                'quantity': quantity,
                'get_total': total
            }
            items.append(item)
                    
            if not product.digital:
                order['shipping'] = True
        except ObjectDoesNotExist:
            logger.warning(f"Product with ID {product_id} not found in database")
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing cart item {product_id}: {e}")
    
    logger.debug(f"Cart items count: {cartItems}")
    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    """
    Get cart data for both authenticated and anonymous users.
    
    Args:
        request: Django HTTP request object
        
    Returns:
        dict: Dictionary containing cart items, order, and items list
    """
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.select_related('product').all()
            cartItems = order.get_cart_items
        except ObjectDoesNotExist:
            logger.error(f"Customer profile not found for user {request.user.username}")
            # Fall back to cookie cart
            cookieData = cookieCart(request)
            return cookieData
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']             
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    """
    Create an order for a guest user (not authenticated).
    
    Args:
        request: Django HTTP request object
        data: Order data including form information
        
    Returns:
        tuple: (customer, order) objects
    """
    logger.info('Processing guest order')
          
    try:
        name = data['form']['name']
        email = data['form']['email']
    except KeyError as e:
        logger.error(f"Missing required field in form data: {e}")
        raise ValueError(f"Missing required field: {e}")
          
    cookieData = cookieCart(request)
    items = cookieData['items']
          
    customer, created = Customer.objects.get_or_create(
        email=email,
        defaults={'name': name}
    )
    
    if not created and customer.name != name:
        customer.name = name
        customer.save()
          
    order = Order.objects.create(
        customer=customer,
        complete=False,
    )
          
    for item in items:
        try:
            product = Product.objects.get(id=item['product']['id'])
                   
            OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity']
            )
        except ObjectDoesNotExist:
            logger.error(f"Product {item['product']['id']} not found while creating order item")
        except (KeyError, ValueError) as e:
            logger.error(f"Error creating order item: {e}")
        
    logger.info(f"Guest order created: Order #{order.id} for {email}")
    return customer, order


