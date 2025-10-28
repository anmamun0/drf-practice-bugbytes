import django_filters
from rest_framework.filters import BaseFilterBackend
from django_filters import rest_framework as filters
from .models import Product, Order

class InStockFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)

# class ProductFilter(django_filters.FilterSet):
#     class Meta:
#         model = Product
#         fields = {
#             'name': ['iexact', 'icontains'], 
#             'price': ['exact', 'lt', 'gt', 'range']
#         }

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at': ['lt', 'gt', 'exact']
        }

class ProductFilter(filters.FilterSet):
    # Char/Text Filters
    product_name = filters.CharFilter(
        field_name='name',       # maps 'product_name' query param to model field 'name'
        lookup_expr='icontains', # performs a case-insensitive "contains" lookup
        label='Product Name',
        help_text='Filter products by name containing this text'
    )
    # Example: /api/products/?product_name=phone

    description = filters.CharFilter(
        lookup_expr='icontains',  # filters description with case-insensitive contains
        label='Description',
        help_text='Filter products by text in description'
    )
    # Example: /api/products/?description=smart

    # Numeric Filters
    price_min = filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',       # greater than or equal to
        label='Minimum Price',
        help_text='Filter products with price >= value'
    )
    # Example: /api/products/?price_min=100

    price_max = filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',       # less than or equal to
        label='Maximum Price',
        help_text='Filter products with price <= value'
    )
    # Example: /api/products/?price_max=500

    price_range = filters.RangeFilter(
        field_name='price',
        label='Price Range',
        help_text='Filter products within a specific price range'
    )
    # Example: /api/products/?price_range_min=100&price_range_max=500

    stock = filters.NumberFilter(
        lookup_expr='exact',     # exact value
        label='Stock Quantity',
        help_text='Filter products with exact stock quantity'
    )
    # Example: /api/products/?stock=10

    # Boolean Filter
    in_stock = filters.BooleanFilter(
        method='filter_in_stock',  # calls custom method for filtering
        label='In Stock',
        help_text='Filter products that are in stock'
    )
    # Example: /api/products/?in_stock=true

    # Custom method filter
    def filter_in_stock(self, queryset, name, value):
        if value:  # filter products where stock > 0
            return queryset.filter(stock__gt=0)
        return queryset

    # Ordering Filter
    ordering = filters.OrderingFilter(
        fields={
            'price': 'price',
            'name': 'name',
            'stock': 'stock'
        },
        field_labels={
            'price': 'Price',
            'name': 'Name',
            'stock': 'Stock'
        },
        label='Ordering'
    )
    # Example: /api/products/?ordering=price       (ascending)
    # Example: /api/products/?ordering=-price      (descending)
    # Can order by multiple fields: ?ordering=-price,name

    class Meta:
        model = Product
        fields = [
            'product_name',      # CharFilter
            'description',       # CharFilter
            'price_min',         # NumberFilter (gte)
            'price_max',         # NumberFilter (lte)
            'price_range',       # RangeFilter
            'stock',             # NumberFilter
            'in_stock',          # BooleanFilter (custom method)
        ]
