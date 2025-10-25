## Django REST Framework - Dynamic Filtering | Overriding `get_queryset()` Method
**Date:** 25 October 2025  
 
---
 
To learn how to perform **dynamic filtering** in Django REST Framework (DRF) by **overriding the `get_queryset()` method** inside class-based views such as `ListAPIView` or `ModelViewSet`.


**Official Docs:** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

<br>

**When to Use `get_queryset()`**

- To filter objects by query parameters (e.g., ?status=active).
- To show user-specific data (e.g., only the logged-in user’s posts).
- To apply conditions dynamically, depending on request context.

<br>

### Lifecycle

`get_queryset(self)` must return a QuerySet.
It can access:
- `self.request` → current HTTP request.
- `self.kwargs` → URL parameters.
- `self.action` → in ViewSet, indicates current action (list, retrieve, etc.).
- Always call `super().get_queryset()` if you extend parent logic.


```py

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

```
> Here set `user=self.request.user` , that means current login user all data will filter and show current login user Orders 

