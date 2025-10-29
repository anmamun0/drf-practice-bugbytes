# Django REST Framework - Django Caching  
**Date:** 29 October 2025  
 
---
> Caching is used to **store frequently accessed data** to improve performance
and reduce database hits.

## Useful Resources Django  
 

- **Redis Python client** : [https://github.com/redis/redis-py](https://github.com/redis/redis-py)
- **Django Redis:** : [github.com/jazzband/django-redis](https://github.com/jazzband/django-redis)
- **DRF Caching Guide** : [https://www.django-rest-framework.org/api-guide/caching/](https://www.django-rest-framework.org/api-guide/caching/)

  
**Practice Code** : [Implement Django caching](https://github.com/anmamun0/drf-practice-BugBytes/commit/4ab514fa19c4f00fe729bdfa88b17296c45801fb) <br>  

  
--- 
<br>

 
# Django Caching Notes

Caching is used to **store frequently accessed data** to improve performance
and reduce database hits.


## 1. Cache Backends

<h6>

| Backend | Description | Usage |
|---------|-------------|-------|
| LocMemCache | In-memory, per-process cache. Only for **development/testing**. | `"BACKEND": "django.core.cache.backends.locmem.LocMemCache"` |
| FileBasedCache | Stores cache in filesystem files. | `"BACKEND": "django.core.cache.backends.filebased.FileBasedCache"` |
| Memcached | Distributed memory cache for production. | `"BACKEND": "django.core.cache.backends.memcached.MemcachedCache"` |
| Redis | Fast, persistent cache, shared across multiple processes/servers. | `"BACKEND": "django_redis.cache.RedisCache"` |
</h6> 

## 2. Example CACHES settings

### 1. LocMemCache (development) 

> Description: In-memory cache stored per process. Fast but not shared across processes or servers. Best for development and testing only.
 
```py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake"
    }
}
```
```py
from django.core.cache import cache

# Set cache
cache.set('my_key', 'my_value', timeout=60)  # 60 seconds
# Get cache
value = cache.get('my_key')
```

### 2. FileBasedCache
> Description: Stores cache in filesystem files. Can persist across server restarts. Slower than memory caches. Note: Good for low-traffic production or small-scale persistence without extra dependencies.
```py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/var/tmp/django_cache",
    }
}
```
### 3. Memcached
> Description: Distributed memory cache. Can be shared across multiple servers. Very fast. Popular for production.

```py
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "127.0.0.1:11211",
    }
}  

```
### 4. Redis
> Description: Persistent, fast key-value store. Can be used as cache and message broker. Supports multiple processes and servers.

```py
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```
 

<br>
<br>
<br>


## 1. Product Model Example

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
```

### 2. Per-View Caching with ListAPIView
```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None

    # Cache the list API for 15 minutes
    @method_decorator(cache_page(60 * 15, key_prefix='product_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
        
    # Simulate slow query
    def get_queryset(self):
        import time
        time.sleep(2)  # simulate heavy query
        return super().get_queryset()
```
- `cache_page(60 * 15, key_prefix='product_list')` caches the response for 15 minutes.
- `get_queryset()` can simulate slow queries; first request will be slow, cached responses are instant.
- Works with any cache backend like LocMemCache, Redis, or Memcached.
 

<br>
<br>
<br>

 

## 3. Using Cache in Views
> Function-Based View
```py
from django.core.cache import cache
from django.shortcuts import render
from .models import Product

def product_list(request):
    products = cache.get('product_list')
    if not products:
        products = Product.objects.all()
        cache.set('product_list', products, 60*15)  # cache for 15 minutes
    return render(request, 'products.html', {'products': products})
```
### Class-Based View with Cache Decorator
```py
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView
from .models import Product

@method_decorator(cache_page(60*15, key_prefix='product_list'), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
```

### 4. Cache Invalidation
> When the data changes (create/update/delete), invalidate the cache:
```py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from django.core.cache import cache

@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache.delete('product_list')  # use the same key as the cache
```
 

- `delete_pattern()` works with Redis but not with LocMemCache.
- Use `cache_page` for view-level caching and `cache.set`/`get` for object-level caching.

--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)