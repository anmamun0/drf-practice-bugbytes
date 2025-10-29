# Django REST Framework - Django REST Framework (DRF) Throttling
**Date:** 29 October 2025  
 
---
Throttling is a mechanism to limit the rate of API requests from clients. It helps protect your API from overuse, abuse, or denial-of-service attacks. DRF provides several built-in throttles and allows custom throttling logic.

## Useful Resources Django  
 

- **Throttling Guide** : [django-rest-framework.org/api-guide/throttling](https://www.django-rest-framework.org/api-guide/throttling/)
 
  
**Practice Code** : [Implement Throttling AnonRateThrottle to limit requests from anonymous users](https://github.com/anmamun0/drf-practice-BugBytes/commit/cd075383e1689e60a3a32af4f9487bd8e64f7bf4) <br>  
**Practice Code** : [Implement Throttling UserRateThrottle to limit requests from authenticated users](https://github.com/anmamun0/drf-practice-BugBytes/commit/723997bc05ee08d0f3b6ac4c6371a584819afb73) <br>  
**Practice Code** : [Implement Throttling ScopedRateThrottle to limit specific view/endpoint request rate control](https://github.com/anmamun0/drf-practice-BugBytes/commit/685c0c2c752f5cd8b2378246d6d3b9afc701c49d) <br>  
**Practice Code** : [Implement Throttling custom UserRateThrottle classes - scope values to differentiate throttle behavior](https://github.com/anmamun0/drf-practice-BugBytes/commit/93c08e6953163e09d16782ad42252ecb2b604ed2) <br>  

  
--- 
<br>

- Prevents excessive requests from a client (anonymous or authenticated).
- Protects server resources and ensures fair usage.
- Supports both short-term and long-term rate limiting.


</h6>

| Throttle Class         | Description                                                      |
| ---------------------- | ---------------------------------------------------------------- |
| **AnonRateThrottle**   | Limits requests from **anonymous (unauthenticated) users**.      |
| **UserRateThrottle**   | Limits requests from **authenticated users**.                    |
| **ScopedRateThrottle** | Allows **per-view or per-endpoint request limits** using scopes. |

<h6>


```py
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle', # for guest user 
        'rest_framework.throttling.UserRateThrottle' # for authenticated user
        'rest_framework.throttling.ScopedRateThrottle', # custom view/endpoint
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '5/day',  # guest user - per day 5 requests
        'user': '20/minute', # authenticated user - per minute 20 requests
    }
}
```

--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)