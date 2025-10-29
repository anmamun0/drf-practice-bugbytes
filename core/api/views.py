from django.db.models import Max
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view ,action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Order, OrderItem, Product, User
from api.serializers import (OrderSerializer, ProductInfoSerializer,
                             ProductSerializer,OrderCreateSerializer,UserSerializer)

from .filters import InStockFilterBackend, OrderFilter, ProductFilter
from .paginations import (CustomLimitOffsetPagination,
                          CustomPageNumberPagination)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.throttling import ScopedRateThrottle

class ProductListAPIView(generics.ListAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope  = 'low'

    queryset = Product.objects.exclude(stock__gt=0)
    serializer_class = ProductSerializer

# Also GET and POST Mehhod
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    # filterset_fields = ('name','price')
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,InStockFilterBackend]
    search_fields = ['name','description'] # ?search=mamun
    ordering_fields = ['name', 'price', 'stock']  # ?ordering=price  # ?ordering=-price  
    # pagination_class = [PageNumberPagination]
    # pagination_class.page_size = 2
    # pagination_class.page_query_param = 'pagenum' # default ?page=2 now ?pagenum=2
    # pagination_class.page_size_query_param = 'size' # if ?size=7 | will load 7 data 
    # pagination_class.max_page_size = 10000 # ?size= | its maximum 10000 data can load 
    
    # pagination_class = LimitOffsetPagination # ?limit=100&offset=400
    # limit=100 → Show 100 records per request.
    # offset=400 → Skip the first 400 records, then start returning data from record 401 onward.
    pagination_class = CustomPageNumberPagination  # only one class here

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

# Just POST Method
class ProductCreateAPIView(generics.CreateAPIView):

    model = Product
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)


# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

# class ProductDetailAPIView(generics.RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_url_kwarg = 'product_id'

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()    

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny] 
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # can also check if POST: if self.request.method == 'POST'
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()

    @action(
        detail=False,
        methods=['get'],
        url_path='user-orders',
        permission_classes=[IsAuthenticated]
    )
    def user_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs
     

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related('items__product')
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    # print(products.aggregate(max_price = Max('price'))) # return dictionary 
    # {'max_price': Decimal('500.050000000000')}
    return Response(serializer.data)

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)


class UserListView(generics.ListAPIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None

    @method_decorator(cache_page(60 * 15, key_prefix='user_list'))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()