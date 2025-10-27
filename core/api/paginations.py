from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'pagenum'          # Example: ?pagenum=3
    page_size_query_param = 'size'        # Example: ?size=10 
    max_page_size = 100
# default: GET ?page=2
# CustomPageNumberPagination: GET /api/products/?pagenum=2&size=10 | second page and load 10 data 
 
class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'
    max_limit = 50
# default: GET ?limit=100&offset=400
# CustomLimitOffsetPagination: GET /api/products/?limit=100&start=400
