# Django REST Framework -  Pagination
**Date:** 27 October 2025  
 
---
> `BaseFilterBackend` in Django REST Framework control how querysets are filtered before being returned to the client.
 
### Useful Resources

- **api-guide-pagination** : [Pagination](https://www.django-rest-framework.org/api-guide/pagination/#pagination)
 
**Practice Code** : [Implement global pagination settings.py using pagination](https://github.com/anmamun0/drf-practice-BugBytes/commit/0f8a63c09c2e9dbf163cb508e474e458ee673bc4) <br>
**Practice Code** : [Customize PageNumberPagination in view.py (page size, query params, max size)](https://github.com/anmamun0/drf-practice-BugBytes/commit/3bd334dae0474579d8a2b92b567efdc32e58974a) <br>
**Practice Code** : [Customize LimitOffsetPaginationin view.py (limit, offset)](https://github.com/anmamun0/drf-practice-BugBytes/commit/0cd7266c7788fc671154b07b0188d1c911229b01) <br>
**Practice Code** : [Customize PageNumberPagination & LimitOffsetPagination in pagination.py](https://github.com/anmamun0/drf-practice-BugBytes/commit/c233024ff16589c59a31f0dc388dc7c94bf2b701) 
 
 

---

<br>
<br>

## 1. Global Pagination (settings.py)

Set default pagination globally for DRF in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
```
- `DEFAULT_PAGINATION_CLASS`: Default pagination class to use.
- `PAGE_SIZE`: Default number of items per page.


<br>

## 2. PageNumberPagination

<h6>

`from rest_framework.pagination import PageNumberPagination` 
 
| Parameter               | Description / Example                                     | Code Example                                   |
| ----------------------- | --------------------------------------------------------- | ---------------------------------------------- |
| **page_size**            | Default number of items per page; e.g., 5                | `page_size = 5`                                |
| **page_query_param**     | Query parameter to change page; e.g., `?page=2`          | `page_query_param = 'page'`                |
| **page_size_query_param**| Query parameter to change page size; e.g., `?size=10`    | `page_size_query_param = 'size'`              |
| **max_page_size**        | Maximum number of items per page; e.g., 100              | `max_page_size = 100`                          |
| **last_page_strings**        | Users don’t need to calculate the last page number manually. It’s especially useful when data size can vary. | `last_page_strings = ('last', 'end', 'final')`  |
| **Usage in View**        | Assign pagination class to view  # only one class here   | `pagination_class = PageNumberPagination/CustomClassName`|
 
</h6>

> paginations.py

```py
from rest_framework.pagination import PageNumberPagination 

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'pagenum'          # Example: ?pagenum=3
    page_size_query_param = 'size'        # Example: ?size=10
    max_page_size = 100                   # Maximum allowable requested page size
    last_page_strings = ('last',)         # Now you can use ?pagenum=last

```
> views.py
```py
# views.py
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination 
from .paginations import CustomPageNumberPagination

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    # serializer_class = PageNumberPagination # default 
    serializer_class = ProductSerializer    # custom
    pagination_class = CustomPageNumberPagination  # Apply custom pagination

```


> Optional Code 
```py
# views.py
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import PageNumberPagination

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination  # Apply buildin pagination 
    pagination_class.page_size = 2
    pagination_class.page_query_param = 'pagenum' # default ?page=2 now ?pagenum=2
    pagination_class.page_size_query_param = 'size' # if ?size=7 | will load 7 data 
    pagination_class.max_page_size = 10000 # ?size= | its maximum 10000 data can load 
```

<br>

## 3. LimitOffsetPagination

- **limit** - Maximum number of items per page; e.g., `?limit=100` 
- **offset** - Number of items to skip; e.g., `?offset=400`
  

```http
GET https://127.0.0.1:8000/accounts?limit=100&offset=400
```
> `limit=100` → Show 100 records per request. <br>
> `offset=400` → Skip the first 400 records, then start returning data from record 401 onward.


<h6>  


| Parameter             | Description / Example                                     | Code Example                                    |
| --------------------- | --------------------------------------------------------- | ----------------------------------------------- |
| **default_limit**      | Default number of items per page; e.g., `?limit=10`      | `default_limit = 10`                            |
| **limit_query_param**  | Query parameter to control page size; e.g., `?limit=50`  | `limit_query_param = 'limit'`                  |
| **offset_query_param** | Query parameter to skip items; e.g., `?offset=100`       | `offset_query_param = 'size'` ?limit=100&size=400  |
| **max_limit**          | Maximum allowed items per page; e.g., `1000`             | `max_limit = 1000`                              |
| **Usage in View**      | Assign pagination class to view                            | `pagination_class = CustomLimitOffsetPagination` |
 

</h6>

> paginations.py
```py
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'           # Example: ?limit=50
    offset_query_param = 'offset'         # Example: ?offset=100
    max_limit = 1000
```
> views.py
```py
from rest_framework.pagination import LimitOffsetPagination
from .pagination import CustomLimitOffsetPagination 

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # pagination_class = LimitOffsetPagination     # default 
    pagination_class = CustomLimitOffsetPagination  # custom 
```


--- 
> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)