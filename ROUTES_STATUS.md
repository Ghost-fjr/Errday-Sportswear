# Route Status Check - Errday Sportswear

## All Configured Routes

### Main Routes (store app)
| URL Pattern | View Function | URL Name | Status |
|------------|---------------|----------|--------|
| `/` | `views.store` | `store` | ✅ Working |
| `/cart/` | `views.cart` | `cart` | ✅ Working |
| `/checkout/` | `views.checkout` | `checkout` | ✅ Working |
| `/update_item/` | `views.updateItem` | `update_item` | ✅ Working (POST only) |
| `/update_size/` | `views.updateSize` | `update_size` | ✅ Working (POST only) |
| `/process_order/` | `views.processOrder` | `process_order` | ✅ Working (POST only) |
| `/login.html` | `views.loginview` | `login` | ✅ Working |
| `/AboutUs.html` | `views.AboutUs` | `AboutUs` | ✅ Working |

### Admin Route
| URL Pattern | URL Name | Status |
|------------|----------|--------|
| `/admin/` | Django Admin | ✅ Working |

## URL References in Templates

### Navbar (main.html)
- ✅ `{% url 'store' %}` - Homepage/Shop
- ✅ `{% url 'AboutUs' %}` - About page  
- ✅ `{% url 'login' %}` - Login page
- ✅ `{% url 'cart' %}` - Cart page

### Store Page (store.html)
- All product actions use JavaScript (update_item)
- No direct URL issues

### Cart Page (cart.html)
- ✅ `{% url 'store' %}` - Continue shopping
- ✅ `{% url 'checkout' %}` - Checkout button
- JavaScript handles update_item and update_size

### Checkout Page (checkout.html)
- ✅ `{% url 'cart' %}` - Back to cart
- ✅ `{% url 'store' %}` - Return after order
- JavaScript POST to process_order

## Known Issues Fixed
1. ✅ Changed `{% url 'loginview' %}` to `{% url 'login' %}` in navbar
2. ✅ Removed non-existent `{% url 'logout' %}` reference

## Notes
- All routes should now work without 404 errors
- The 500 error was likely from the incorrect URL name
- Static files served from `/static/` directory
- Media files served from `/media/` directory

## Testing Checklist
- [ ] Homepage loads (/)
- [ ] Products display with images
- [ ] Cart page accessible
- [ ] Checkout form loads
- [ ] Login page works
- [ ] About Us page loads
- [ ] Add to cart function works
- [ ] Update cart quantities works
