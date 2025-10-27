# Django REST Framework -  Advanced Filtering with `django_filters`
**Date:** 27 October 2025  
 
---
> `django-filter` provides a powerful and declarative way to **filter querysets** in Django REST Framework APIs.   Instead of manually parsing query parameters, you can define filters using `FilterSet` classes for clean, readable, and reusable logic.

 
### Useful Resources

- **django-rest-framework-filtering** : [Documenting your API](https://www.django-rest-framework.org/api-guide/filtering/#generic-filtering)
- **django-filter-readthedocs** : [django-filter.readthedocs.io](https://django-filter.readthedocs.io/en/stable/) 

**Practice Code** :[Simple equality-based filtering using filterset_fields](https://github.com/anmamun0/drf-practice-BugBytes/commit/21ff6232953366404b03a2046b10f2edb8186f22)
**Practice Code** :[Advanced filtering using Meta dictionary with multiple lookups](https://github.com/anmamun0/drf-practice-BugBytes/commit/e170a7f4b08de51a21eaa4c921f1ec3f71d8be32)
**Practice Code** : [Advanced explicit filter definition using django_filters](https://github.com/anmamun0/drf-practice-BugBytes/commit/9ef5f55d0bcf4fc0bf089d9180e2909769e6434d)


---
<br>


### 1. Simple Equality-Based Filtering using `filterset_fields`

```python
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ('name', 'price')  # simple equality filters


```

```http
/api/products/?name=Phone
/api/products/?price=500
```
> Automatically provides exact filtering on the specified fields.





### 2. Advanced Filtering using Meta Dictionary (Multiple Lookups)
```py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'price': ['exact', 'lt', 'gt', 'range']
        }
```
```http
/api/products/?name__iexact=phone
/api/products/?name__icontains=pro
/api/products/?price__lt=1000
/api/products/?price__range=500,1500
``` 
- Declarative and automatic lookups
- Cleaner and DRY (Don’t Repeat Yourself)
- Automatically supports multiple comparison operators





### 3. Advanced Explicit Filter Definition

```py
import django_filters
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Product Name',
        help_text='Filter products by name containing this text'
    )
    price = django_filters.RangeFilter()
    is_available = django_filters.BooleanFilter()
    created_at = django_filters.DateFromToRangeFilter()
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    ordering = django_filters.OrderingFilter(fields=['price', 'name', 'created_at'])

    class Meta:
        model = Product
        fields = ['name', 'price', 'is_available', 'category']
```
```json
/api/products/?name=phone
/api/products/?price_min=100&price_max=500
/api/products/?is_available=true
/api/products/?created_at_after=2024-01-01&created_at_before=2024-12-31
/api/products/?category=2
/api/products/?ordering=-price,name
```
 
- Explicit control over query param names (field_name=)
- Can rename parameters, add help text, and control labels
- Supports range, date, boolean, and ordering filters



<h6>

 | **Filter Type**             | **Purpose**                            | **Auto Query Parameters**            | **Equivalent Lookups**                              | **Example API Call**                                                                    |
| --------------------------- | -------------------------------------- | ------------------------------------ | --------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `CharFilter`                | Text-based matching                    | Same as field name                   | `exact`, `iexact`, `icontains`, `istartswith`, etc. | `/api/products/?name=iphone` or `/api/products/?name__icontains=phone`                  |
| `NumberFilter`              | Numeric field comparison               | Same as field name                   | `exact`, `lt`, `gt`, `lte`, `gte`                   | `/api/products/?price__lt=500`                                                          |
| `BooleanFilter`             | True/False filtering                   | Same as field name                   | `exact`                                             | `/api/products/?is_available=true`                                                      |
| `ChoiceFilter`              | Filter by one choice                   | Same as field name                   | `exact`                                             | `/api/users/?role=student`                                                              |
| `MultipleChoiceFilter`      | Filter by multiple values              | Same as field name (comma-separated) | `in`                                                | `/api/products/?category=mobile,laptop`                                                 |
| `RangeFilter`               | Numeric range filtering                | `_min`, `_max`                       | `gte`, `lte`                                        | `/api/products/?price_min=100&price_max=500`                                            |
| `DateFilter`                | Exact or relative date filtering       | Same as field name                   | `exact`, `lt`, `gt`, `range`, etc.                  | `/api/orders/?created_at__gt=2025-01-01`                                                |
| `DateFromToRangeFilter`     | Date range filtering                   | `_after`, `_before`                  | `gte`, `lte`                                        | `/api/orders/?created_at_after=2025-01-01&created_at_before=2025-05-01`                 |
| `TimeFilter`                | Time field comparison                  | Same as field name                   | `exact`, `lt`, `gt`, etc.                           | `/api/events/?start_time__gte=09:00`                                                    |
| `TimeRangeFilter`           | Time range filtering                   | `_after`, `_before`                  | `gte`, `lte`                                        | `/api/events/?start_time_after=09:00&start_time_before=12:00`                           |
| `DateTimeFilter`            | DateTime comparison                    | Same as field name                   | `exact`, `lt`, `gt`, etc.                           | `/api/logs/?created_at__gte=2025-01-01T00:00:00`                                        |
| `DateTimeFromToRangeFilter` | DateTime range filtering               | `_after`, `_before`                  | `gte`, `lte`                                        | `/api/logs/?created_at_after=2025-01-01T00:00:00&created_at_before=2025-01-05T23:59:59` |
| `ModelChoiceFilter`         | Foreign key single selection           | Same as field name                   | `exact`                                             | `/api/products/?category=3`                                                             |
| `ModelMultipleChoiceFilter` | Foreign key multiple selection         | Same as field name (comma-separated) | `in`                                                | `/api/products/?category=1,2,3`                                                         |
| `OrderingFilter`            | Sort results by field                  | Same as field name                   | `order_by`                                          | `/api/products/?ordering=-price,name`                                                   |
| `AllValuesFilter`           | Filter using all distinct values in DB | Same as field name                   | `exact`                                             | `/api/books/?language=English`                                                          |
| `UUIDFilter`                | UUID field filtering                   | Same as field name                   | `exact`                                             | `/api/items/?uuid=550e8400-e29b-41d4-a716-446655440000`                                 |
| `SlugFilter`                | Slug field filtering                   | Same as field name                   | `exact`, `icontains`                                | `/api/blogs/?slug=python-basics`                                                        |
| `IsoDateTimeFilter`         | ISO format datetime filter             | Same as field name                   | `exact`, `lt`, `gt`, etc.                           | `/api/logs/?timestamp__lt=2025-10-20T12:00:00Z`                                         |

</h6>


--- 
> [`Author`](https://github.com/anmamun0)
> [`Project`](drf-practice-BugBytes)