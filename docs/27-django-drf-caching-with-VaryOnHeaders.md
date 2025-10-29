# Django REST Framework - Django Caching  
**Date:** 29 October 2025  
 
---
 Django provides caching mechanisms to improve performance by storing the result of expensive computations or database queries. When caching views that depend on headers like Authorization, it is crucial to vary the cache key based on the header to prevent leaking user-specific data.

## Useful Resources Django  
 

- **Caching very-headers** : [docs.djangoproject.com/decorators/#very-headers](https://docs.djangoproject.com/en/5.1/topics/http/decorators/#very-headers)
 
  
**Practice Code** : [Implement Django caching very-headers](https://github.com/anmamun0/drf-practice-BugBytes/commit/8ec84b19b214e6e64cc20bf0628bd6e80792b281) <br>  

  
--- 
<br>
 

### 2.  Simple Cache
```py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.generics import ListAPIView
from api.models import User
from api.serializers import UserSerializer

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None

    @method_decorator(cache_page(60*15, key_prefix='user_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```
- Caches the list of users for 15 minutes.
- Key prefix ensures cache isolation.


### 3.   Cache Varying by Authorization Header
```py
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response

class ProfileView(APIView):

    @method_decorator(vary_on_headers('Authorization'))
    def get(self, request):
        # Response cache will vary per user token
        return Response({"username": request.user.username})
```

- `@vary_on_headers('Authorization')` ensures that cache is separated per unique Authorization header.
- Prevents user-specific data leakage.

### 4. Signals: Invalidate Cache
```py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import User
from django.core.cache import cache

@receiver([post_save, post_delete], sender=User)
def invalidate_user_cache(sender, instance, **kwargs):
    cache.delete_pattern('*user_list*')
```

- Automatically clears cached user lists when a user is created, updated, or deleted.


--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)