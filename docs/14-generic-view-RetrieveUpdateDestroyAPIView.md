# Django REST Framework - JWT Refresh Tokens & Authentication
**Date:** 26 October 2025  
 
---

## RetrieveUpdateDestroyAPIView

RetrieveUpdateDestroyAPIView is a DRF generic view that combines three operations for a single object:

- `Retrieve` → Fetch a single instance of a model.
- `Update` → Modify an existing instance (partial or full update).
- `Destroy` → Delete an instance.

> This view is ideal for endpoints where you want CRUD operations on a single object.

<br>

Example
```py
from rest_framework import generics
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()    
```