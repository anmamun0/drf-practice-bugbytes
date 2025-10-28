# Django REST Framework -  ViewSets & Routers - ViewSet Filters, Actions & isort Formatting
**Date:** 28 October 2025  
 
---
> `ViewSets` combine the logic for multiple related views CRUD(like list, create, retrieve, update, delete) into a single class.
 
### Useful Resources

- **Summary of rest-framework** : [cdrf.co](https://www.cdrf.co/)
- **official-rest-framework** : [django-rest-framework.org](https://www.django-rest-framework.org/)
 
**Practice Code** : [Implement ViewSets and Routers in Django REST Framework](https://github.com/anmamun0/drf-practice-BugBytes/commit/2edae06e6e08d12e1933f6640248bb97f04d9a8a) <br> 
 
**`viewsets`**  -  `GenericViewSet`, `ModelViewSet`,  `ReadOnlyModelViewSet` <br>
**`routers`**  - `DefaultRouter`, `SimpleRouter`, `CustomRouter`

---

<br>
  


## 1. Implement Filter in `viewsets.ModelViewSet`

>  Filtering allows users to retrieve a subset of data based on query parameters.  
DRF integrates seamlessly with **django-filter** for building advanced filtering systems.

 
```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from .filters import OrderFilter

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
``` 
> filters.py
```py
import django_filters 
from .models import Order

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact']
        }
```

<br>



## 2. Actions using @action Decorator in viewsets.ModelViewSet
 
> `@action` decorator adds custom endpoints to a ViewSet. 

```py
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='user-orders',
        permission_classes=[IsAuthenticated],
    )
    def user_orders(self, request): 
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
```
### Key Points
- `detail=False` → For list-level routes (like `/orders/user-orders/`)
- `detail=True` → For detail-level routes (like `/orders/{id}/user_orders/`)
- You can override: `permission_classes`, `serializer_class`, `pagination_class`


<br>


## 3. isort Formatting to Python File

**isort** : [pycqa.github.io/isort](https://pycqa.github.io/isort/)

> automatically sorts and groups Python imports for better readability and maintainability.

Installation
```
pip install isort
```

Usage: Run isort on a specific file or your entire project:
> run in terminal
```sh
isort views.py
isort .
```
 

--- 
> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)