"""
Custom middleware for security headers and request processing.
"""


class SecurityHeadersMiddleware:
    """
    Adds comprehensive security headers to all responses.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy for payment gateway integration
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com; "
            "style-src 'self' 'unsafe-inline' https://stackpath.bootstrapcdn.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://stackpath.bootstrapcdn.com; "
            "frame-ancestors 'self' https://*.helcim.app https://*.myhelcim.com; "
            "connect-src 'self';"
        )
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
