"""
Views for the e-commerce store application.
"""
import json
import logging
import datetime
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from django.core.exceptions import ValidationError

from .models import Order, OrderItem, Product, Customer, ShippingAddress
from .utils import cookieCart, cartData, guestOrder

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def loginview(request):
    """
    Handle user login for customer accounts.
    
    GET: Display login form
    POST: Authenticate user and redirect to store
    
    Returns:
        Rendered login page with error status if applicable
    """
    error = ""
    if request.method == "POST":
        username = request.POST.get('userName', '')
        password = request.POST.get('pwd', '')
        
        if not username or not password:
            error = "yes"
            logger.warning("Login attempt with missing credentials")
        else:
            user = authenticate(username=username, password=password)
            if user:
                try:
                    # Check if user has customer profile
                    customer = Customer.objects.get(user=user)
                    login(request, user)
                    logger.info(f"User {username} logged in successfully")
                    return redirect('store')
                except Customer.DoesNotExist:
                    error = "yes"
                    logger.warning(f"User {username} has no customer profile")
            else:
                error = "yes"
                logger.warning(f"Failed login attempt for username: {username}")
            
    return render(request, 'store/login.html', {'error': error})


def store(request):
    """
    Display the main product catalog page.
    
    Shows all active products with cart item count for the user.
    
    Returns:
        Rendered store page with products and cart information
    """
    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    context = {'products': products, 'cartItems': cartItems}
    
    logger.debug(f"Store page accessed with {products.count()} products")
    return render(request, 'store/store.html', context)
   

def cart(request):
    """
    Display the shopping cart page.
    
    Shows cart items for both authenticated and guest users.
    
    Returns:
        Rendered cart page with items and order summary
    """
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']             
    items = data['items']
    
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    logger.debug(f"Cart accessed with {cartItems} items")
    return render(request, 'store/cart.html', context)



def checkout(request):
    """
    Display the checkout page.
    
    Shows order summary and shipping information form.
    
    Returns:
        Rendered checkout page with order details
    """
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']             
    items = data['items']
    
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    logger.debug(f"Checkout accessed with {cartItems} items")
    return render(request, 'store/checkout.html', context)




@require_POST
def updateItem(request):
    """
    Update cart item quantity via AJAX.
    
    Expects JSON payload with productId and action ('add' or 'remove').
    Handles both authenticated and anonymous users.
    
    Returns:
        JSON response confirming the update
    """
    try:
        data = json.loads(request.body)
        product_id = data.get('productId')
        action = data.get('action')
        
        if not product_id or not action:
            return JsonResponse({'error': 'Missing productId or action'}, status=400)
        
        logger.info(f"Update item request: Product {product_id}, Action: {action}")
        
        if not request.user.is_authenticated:
            # Handle cookie-based cart for anonymous users
            return JsonResponse({'message': 'Item updated in cookie cart'}, safe=False)
        
        # Handle database cart for authenticated users
        customer = request.user.customer
        product = get_object_or_404(Product, id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            product=product
        )
        
        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
            
        order_item.save()
        
        if order_item.quantity <= 0:
            order_item.delete()
            logger.info(f"Removed product {product_id} from cart")
        
        return JsonResponse({'message': 'Item was updated', 'quantity': order_item.quantity if order_item.quantity > 0 else 0}, safe=False)
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON in updateItem request")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Customer.DoesNotExist:
        logger.error(f"Customer profile not found for user {request.user.username}")
        return JsonResponse({'error': 'Customer profile not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating cart item: {str(e)}")
        return JsonResponse({'error': 'Server error'}, status=500)

@require_POST
def updateSize(request):
    """
    Update product size selection.
    
    Note: This updates the product's size, not the order item.
    Consider refactoring to update OrderItem size instead.
    
    Returns:
        JSON response with success status
    """
    try:
        product_id = request.POST.get('productId')
        selected_size = request.POST.get('selectedSize')
        
        if not product_id or not selected_size:
            return JsonResponse({'error': 'Missing parameters'}, status=400)
        
        product = get_object_or_404(Product, id=product_id)
        product.size = selected_size
        product.save()
        
        logger.info(f"Updated product {product_id} size to {selected_size}")
        return JsonResponse({'success': True})
        
    except Exception as e:
        logger.error(f"Error updating size: {str(e)}")
        return JsonResponse({'error': 'Failed to update size'}, status=500)


@csrf_exempt
@require_POST
def processOrder(request):
    """
    Process and complete an order.
    
    Validates order total, creates shipping address if needed,
    and marks order as complete.
    
    Returns:
        JSON response confirming order completion
    """
    try:
        transaction_id = str(datetime.datetime.now().timestamp())
        data = json.loads(request.body)
        
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            customer, order = guestOrder(request, data)
        
        # Validate order total
        submitted_total = Decimal(str(data['form']['total']))
        calculated_total = Decimal(str(order.get_cart_total))
        
        order.transaction_id = transaction_id
        
        # Only complete if totals match (within 0.01 for rounding)
        if abs(submitted_total - calculated_total) < Decimal('0.01'):
            order.complete = True
            logger.info(f"Order #{order.id} completed with transaction {transaction_id}")
        else:
            logger.warning(f"Order total mismatch: submitted={submitted_total}, calculated={calculated_total}")
            return JsonResponse({'error': 'Order total mismatch'}, status=400)
        
        order.save()
        
        # Create shipping address if physical products exist
        if order.shipping and 'shipping' in data:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping'].get('address', ''),
                city=data['shipping'].get('city', ''),
                state=data['shipping'].get('state', ''),
                zipcode=data['shipping'].get('zipcode', ''),
            )
            logger.info(f"Shipping address created for order #{order.id}")
        
        return JsonResponse({'message': 'Payment complete!', 'transaction_id': transaction_id}, safe=False)
        
    except json.JSONDecodeError:
        logger.error("Invalid JSON in processOrder")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except KeyError as e:
        logger.error(f"Missing required field in processOrder: {e}")
        return JsonResponse({'error': f'Missing required field: {e}'}, status=400)
    except Customer.DoesNotExist:
        logger.error("Customer not found in processOrder")
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Exception as e:
        logger.error(f"Error processing order: {str(e)}")
        return JsonResponse({'error': 'Server error'}, status=500)





def AboutUs(request):
    """
    Display the About Us page.
    
    Returns:
        Rendered About Us page
    """
    logger.debug("About Us page accessed")
    return render(request, 'store/AboutUs.html') 
     


  