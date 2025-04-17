from rest_framework.throttling import AnonRateThrottle

class LoginThrottle(AnonRateThrottle):
    scope = 'login'
    rate = '10/minute'  # Limit to 10 requests per minute
    
