## Django REST Framework - Generic Views (ListAPIView & RetrieveAPIView)
**Date:** 25 October 2025  
 
---
 
### Overview 
This video covered the **Generic Views** in Django REST Framework — focusing on how `ListAPIView` and `RetrieveAPIView` work to handle read-only API endpoints efficiently.  

**Official Docs:** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

<br>

  
###  What I Learned

**1. Understanding Generic Views**
- Generic views are **pre-built DRF views** designed for common API operations like listing, retrieving, creating, updating, or deleting objects.
- They combine **Mixins** (which add behavior) and **GenericAPIView** (which provides the foundation such as queryset, serializer, and pagination support).

<br>

**2. About `ListAPIView`**
- Used for displaying a **list of objects** from the database.
- Internally based on `ListModelMixin` and `GenericAPIView`.
- Commonly used for endpoints that return all instances of a model (like listing all students, products, or posts).

<br>

**3. About `RetrieveAPIView`**
- Used for fetching a **single record** from the database.
- Internally based on `RetrieveModelMixin` and `GenericAPIView`.
- Useful when an API needs to return details of a single object by its `id`, `slug`, or another lookup field.
- lookup_url_kwarg 

```py
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'
```
```py
path('products/<int:product_id>/', views.ProductDetailAPIView.as_view()),
```

<br>

**When It’s Used**
- When we need **read-only** API endpoints.
- `ListAPIView` → For listing multiple resources.  
- `RetrieveAPIView` → For retrieving one specific resource.
- Ideal when we do not need create, update, or delete functionality.

  

<br>
<br>

### Future Explanation Topics

In future videos, I will explain:
- `ListCreateAPIView`
- `RetrieveUpdateDestroyAPIView`
- How mixins (`CreateModelMixin`, `UpdateModelMixin`, etc.) combine to make flexible APIs.
- How to override and customize default generic behavior.

