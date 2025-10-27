# Django REST Framework -  SearchFilter & OrderingFilter
**Date:** 27 October 2025  
 
---
> `SearchFilter` and `OrderingFilter` are built-in filter backends in Django REST Framework that allow simple, dynamic querying on API results without creating custom FilterSet classes.
 
### Useful Resources

- **django-rest-framework-searchfilter** : [SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/#searchfilter)
- **django-rest-framework-orderingfilter** : [OrderingFilter](https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter) 

**Practice Code** :[Implement Search Filters in api, use filters.SearchFilter rest_framework backend](https://github.com/anmamun0/drf-practice-BugBytes/commit/5f2ada4458ce6a4f3f20210ad6c65602c7df2d26) <br>
**Practice Code** :[Implement Ordering Filters in api, use filters.OrderingFilter rest_framework backend](https://github.com/anmamun0/drf-practice-BugBytes/commit/99c06bfce5e8a26a0ec26cfd155fea7fbdd5e46a) 


### Library
```py
from rest_framework import filters
```

---

<br>


## 1. SearchFilter 
Add SearchFilter to your view or globally in DRF settings.
```py
from rest_framework import generics, filters
from .models import Product
from .serializers import ProductSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
```
  
```http
/api/products/?search=phone	            // Searches for products where name or description contains “phone”
/api/products/?search=Samsung Galaxy	//  multiple keywords
/api/products/?search="exact match"	    // exact match using quotes
```


```py
 search_fields = ['name', 'description', '^brand', '=sku', '$tags', '@content']
```


 <h6>
  
 | Prefix   | Lookup Type   | Description                                  | Example Query                                                     |
| -------- | ------------- | -------------------------------------------- | ----------------------------------------------------------------- |
| `^`      | `istartswith` | Case-insensitive "starts with" search  | `/api/products/?search=sam` → matches **Samsung**                 |
| `=`      | `iexact`      | Case-insensitive exact match           | `/api/products/?search=iphone` → matches **iPhone** only          |
| `$`      | `iregex`      | Regex-based pattern search             | `/api/products/?search=.*Pro$` → matches **MacBook Pro**          |
| `@`      | `search`      | Full-text search (PostgreSQL only)     | `/api/products/?search=smartphone`                                |
| *(none)* | `icontains`   | Case-insensitive substring match *(default)* | `/api/products/?search=phone` → matches **iPhone**, **Headphone** |

 </h6> 




<br>
<br>





## 2. OrderingFilter 
OrderingFilter allows users to dynamically sort API results using query parameters.

```py
from rest_framework import generics, filters

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'name', 'created_at']
    ordering = ['name']  # default ordering
``` 

```http 
/api/products/?ordering=price	        // Sorts by price ascending
/api/products/?ordering=-price	        // Sorts by price descending
/api/products/?ordering=name,price      // Sorts first by name, then price
```




--- 
> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)