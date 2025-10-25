# Django REST Framework - Django REST Framework – APIView Class
**Date:** 25 October 2025  
 
---
 
**Official Docs:** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

In this video, the **APIView class** from Django REST Framework (DRF) was introduced as the **base class** for building fully custom API endpoints.  
It provides **low-level control** over request handling while still supporting DRF’s request/response, authentication, and permission system.

<br>
   

```py
from rest_framework.views import APIView
class ProductInfoAPIView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, world!'})

    def post(self, request):
        name = request.data.get('name', 'Guest')
        return Response({'message': f'Hello, {name}!'})

    def put(self, request): 
        ... pass

    def delete(self, request): 
        ... pass
```
 