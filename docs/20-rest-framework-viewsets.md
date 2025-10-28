# Django REST Framework -  ViewSets & Routers
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
<br>
 
## Types of ViewSets

<h6>
 
| ViewSet Type       | Description                                                                               | Use Case                                  |
| ------------------ | ----------------------------------------------------------------------------------------- | ----------------------------------------- |
| **ViewSet**        | The base class — you must explicitly define each method (`list`, `retrieve`, etc.).       | When you want full manual control.        |
| **GenericViewSet** | Extends `ViewSet` and works with DRF mixins (`ListModelMixin`, `CreateModelMixin`, etc.). | When you need specific CRUD actions only. |
| **ModelViewSet**   | Combines `GenericViewSet` + all CRUD mixins automatically.                                | Most commonly used (for complete CRUD).   |

</h6>

## Common ViewSet ModelViewSet Actions

<h6>

| HTTP Method             | Action Name        | Description              |
| ----------------------- | ------------------ | ------------------------ |
| `GET /objects/`         | `list()`           | Retrieve all objects     |
| `GET /objects/{id}/`    | `retrieve()`       | Retrieve single object   |
| `POST /objects/`        | `create()`         | Add new object           |
| `PUT /objects/{id}/`    | `update()`         | Replace entire object    |
| `PATCH /objects/{id}/`  | `partial_update()` | Update part of an object |
| `DELETE /objects/{id}/` | `destroy()`        | Delete object            |

</h6>


## Example: Using ModelViewSet

> views.py
```py
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

## Routers

Routers automatically generate URL patterns for ViewSets.
You don’t need to manually define urlpatterns for each route.

> urls.py
```py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')

urlpatterns = []
urlpatterns += router.urls

```

<br>

### 8. Custom Actions in ViewSets
```py
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Custom action for single object
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        product = self.get_object()
        product.is_published = True
        product.save()
        return Response({'status': 'Product published!'})

    # Custom action for entire collection
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = Product.objects.filter(is_featured=True)
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
```


--- 
> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)