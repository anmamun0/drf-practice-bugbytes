# Django REST Framework - Django REST Framework: Customising Permissions in Generic Views & REST Client Extension
**Date:** 26 October 2025  
 
---
 
**Official Docs:** [cdrf.co/3.11/rest_framework.viewsets/GenericViewSet](https://www.cdrf.co/3.11/rest_framework.viewsets/GenericViewSet.html)

 

### Adding Custom Permissions in Generic Views

In GenericAPIView or its subclasses (like ListAPIView, RetrieveAPIView ), you can control access using:

```py
permission_classes = [IsAuthenticated]
```

> Example 

```py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
# Also GET and POST Mehhod
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
```

<br>
<br>
<br>

### Example api.http File

This file helps you make API calls directly from `VSCode` — `no Postman` needed.
<br>

**Extensions :** -  `REST Client`

```http
### Get all items
GET http://127.0.0.1:8000/api/items/

### Get single item
GET http://127.0.0.1:8000/api/items/1/

### Create item
POST http://127.0.0.1:8000/api/items/
Content-Type: application/json

{
  "name": "New Item",
  "price": 100
}
```
> Just click `Send Request` above any line starting with `GET` or `POST` to run it.