# Django REST Framework -  Custom Filter Backends
**Date:** 27 October 2025  
 
---
> `BaseFilterBackend` in Django REST Framework control how querysets are filtered before being returned to the client.
 
### Useful Resources

- **Custom Filter Backends** : [Custom Filter Backends](https://www.django-rest-framework.org/api-guide/filtering/#custom-generic-filtering)
 
**Practice Code** :[Implement Custom Filter Backends in Django REST Framework](https://github.com/anmamun0/drf-practice-BugBytes/commit/1fd8325899c724c4bb6237c3f9d1dc5be37313d2) <br>

 
### Django REST Framework Filtering Overview

> filters.py
```py
from rest_framework import filters
```
> views.py
```py
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
```
 


<h6>

# Django REST Framework Filtering Overview

| Library / Backend | Backend Class / Filter       | Purpose / Use Case |
|------------------|-----------------------------|------------------|
| `django_filters.rest_framework` | `DjangoFilterBackend` | Fine-grained, field-level filtering using `FilterSet` classes. Supports exact, range, icontains, and other lookup expressions. |
| `rest_framework.filters` | `SearchFilter` | Text search across specified fields (`search_fields`). |
| `rest_framework.filters` | `OrderingFilter` | Allows ordering results by specified fields (`ordering_fields`). |
| `rest_framework.filters` | `BaseFilterBackend` | Base class for creating **custom filter backends**. You override `filter_queryset(self, request, queryset, view)` to implement custom filtering logic. |

</h6>


---

<br>
<br>

### Filter products by availability 
```http
(?available=true or ?available=false).
```
```py
from rest_framework import filters

class AvailabilityFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        available = request.query_params.get('available')
        if available is not None:
            if available.lower() == 'true':
                return queryset.filter(stock__gt=0)
            elif available.lower() == 'false':
                return queryset.filter(stock__lte=0)
        return queryset
```
<br>

### Apply the Filter

```py
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from .filters import AvailabilityFilterBackend

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [AvailabilityFilterBackend]
```
<br>

### Multiple Custom Parameters 

> Filter by both min_price and max_price manually.

```py
class PriceRangeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset
```
```py
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [AvailabilityFilterBackend, PriceRangeFilterBackend]

```

<br>

### Combining Custom and Built-in Filters

> You can mix your custom filters with built-in ones like SearchFilter or OrderingFilter.
```py
from rest_framework import filters

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        AvailabilityFilterBackend,
        PriceRangeFilterBackend,
    ]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name']
```
<br>
<br>

### Schema Integration

> To make your custom filters visible in DRF Spectacular or `Swagger docs`, you can define `get_schema_fields()` or use `drf-spectacular` annotations.

```py
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes

class AvailabilityFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        available = request.query_params.get('available')
        if available:
            queryset = queryset.filter(stock__gt=0 if available.lower() == 'true' else 0)
        return queryset

    def get_schema_fields(self, view):
        return [
            OpenApiParameter(
                name='available',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter products by availability (true/false)',
            ),
        ]

```



--- 
> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)