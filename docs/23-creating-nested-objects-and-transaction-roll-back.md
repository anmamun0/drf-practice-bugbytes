# Django REST Framework -  Django REST Framework: Creating Nested Objects with create() Method
**Date:** 28 October 2025  
 
---
> `ViewSets` combine the logic for multiple related views CRUD(like list, create, retrieve, update, delete) into a single class.
 
## Useful Resources Django Transactions

- **Transactions Documentation (official):** [Controlling Transactions Explicitly](https://docs.djangoproject.com/en/5.2/topics/db/transactions/#controlling-transactions-explicitly)
- **Database Transactions Overview:** [Django Database Transactions](https://docs.djangoproject.com/en/5.2/ref/databases/#transactions)
- **DRF + Transactions Example:** [DRF Transactions](https://www.django-rest-framework.org/topics/transactions/)


**Practice Code** : [Creating Nested Objects and Overriding serializer create() method]([https://github.com/anmamun0/drf-practice-BugBytes/commit/2edae06e6e08d12e1933f6640248bb97f04d9a8a](https://github.com/anmamun0/drf-practice-BugBytes/commit/a14024782ec3530ce11a7e86e43071c891c1bab9)) <br>  

**`django.db transaction`**  -  `atomic()`,  `set_autocommit`, `get_autocommit`, `set_rollback()`,  `get_rollback()` ,`on_commit()` <br>
 

--- 
<br>
  
 ## 1. Model

 ```py
 from django.db import models
from django.contrib.auth.models import User
import uuid

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

 ```


## 2. Serializers

2.1 Product Serializer
> Used for read purposes in nested serialization.
```py
from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'description']

```

### 2.2 OrderItem Nested Serializer
> Used inside the Order serializer for nested creation.
```py
class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
```


## 2.3 Order Create Serializer

> Handles nested creation of Order and OrderItems.
```py
from django.db import transaction

class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        # Transaction ensures atomic creation
        with transaction.atomic():
            order = Order.objects.create(user=user)
            OrderItem.objects.bulk_create([
                OrderItem(order=order, **item) for item in items_data
            ])
        return order
```
### 2.4 Order Read Serializer

> Returns nested order with items info and product details.
```py
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'created_at', 'items']
```

<br>


## 3. ViewSet

```py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```



## 4. Example POST Request (Nested Creation)

```json
POST /api/orders/

{
    "items": [
        {"product": 1, "quantity": 2},
        {"product": 3, "quantity": 1}
    ]
}

```

> Response:
```json
{
    "order_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "user": 1,
    "created_at": "2025-10-28T10:20:30Z",
    "items": [
        {"product": {"id":1,"name":"Phone","price":"500.00","stock":10,"description":"Smartphone"},"quantity":2},
        {"product": {"id":3,"name":"Laptop","price":"1200.00","stock":5,"description":"Gaming Laptop"},"quantity":1}
    ]
}
```

<br>

## transaction.atomic()

> transaction.atomic() in Django is a database transaction context manager that treats multiple database operations as a single atomic unit. Simply put:
 

- Atomic = “all or nothing”
- If any error occurs inside the transaction, all changes are rolled back.
- No query or save inside the block will persist unless the entire block executes successfully.


```py
from django.db import transaction
from .models import Order, OrderItem

with transaction.atomic():
    order = Order.objects.create(user=user)
    OrderItem.objects.create(order=order, product=product1, quantity=2)
    OrderItem.objects.create(order=order, product=product2, quantity=1)
    # If an error occurs here, neither the order nor the items will be saved
```

If creating a single order fails at any step, the entire order and its items are not saved.

<h6> 
 
| Method/Context     | Purpose                                             |
| ------------------ | --------------------------------------------------- |
| `atomic()`         | Wrap code block in a transaction                    |
| `set_autocommit()` | Enable/disable autocommit                           |
| `get_autocommit()` | Check current autocommit status                     |
| `set_rollback()`   | Mark current transaction to rollback                |
| `get_rollback()`   | Check if current transaction is marked for rollback |
| `on_commit()`      | Register callback to run after successful commit    |

</h6>

 

--- 
> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)