import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        # fields = ('name','price')  # default :  exact
        fields = {
            'name': ['iexact', 'icontains'], 
            'price': ['exact', 'lt', 'gt', 'range']
        }