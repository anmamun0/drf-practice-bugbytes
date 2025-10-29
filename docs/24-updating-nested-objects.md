# Django REST Framework -  Implemented nested object creation using DRF create() with transaction safety.
**Date:** 29 October 2025  
 
---
> let’s move on to the update process (`PUT`/`PATCH`) —
## Useful Resources Django Transactions

- **Transactions Documentation (official):** [Controlling Transactions Explicitly](https://docs.djangoproject.com/en/5.2/topics/db/transactions/#controlling-transactions-explicitly)
- **Database Transactions Overview:** [Django Database Transactions](https://docs.djangoproject.com/en/5.2/ref/databases/#transactions)
- **DRF + Transactions Example:** [DRF Transactions](https://www.django-rest-framework.org/topics/transactions/)


**Practice Code** : [pdating Nested Objects and Overriding serializer update() method and views (get_serializer_class(), perform_create())](https://github.com/anmamun0/drf-practice-BugBytes/blob/main/docs/23-creating-nested-objects-and-transaction-roll-back.md) <br>  

 

--- 
<br>
  
 ## 1. Model 
 ```py
import uuid
from django.db import models
from django.contrib.auth.models import User

STATUS = ( ('Pending', 'Pending'), ('Shipped', 'Shipped'),('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'),)

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
    status = models.CharField(max_length=20, choices=STATUS, default='Pending')

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
```



## 2. Nested Update Serializer (with status included)
> We’ll modify the serializer to handle nested updates transactionally — meaning if one update fails, the whole transaction rolls back.
```py
from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem

class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'status']
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

class OrderUpdateSerializer(serializers.ModelSerializer):
    items = OrderItemUpdateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['items']

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])

        with transaction.atomic():
            existing_items = {item.id: item for item in instance.items.all()}

            for item_data in items_data:
                item_id = item_data.get('id', None)
                if item_id and item_id in existing_items:
                    # Update existing OrderItem
                    order_item = existing_items[item_id]
                    order_item.product = item_data.get('product', order_item.product)
                    order_item.quantity = item_data.get('quantity', order_item.quantity)
                    order_item.status = item_data.get('status', order_item.status)
                    order_item.save()
                else:
                    # Create new OrderItem
                    OrderItem.objects.create(order=instance, **item_data)

        return instance
```

## 3. Update OrderViewSet
> We now add this serializer for the update operations:
```py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return OrderUpdateSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```
## 4. Example Request — Full Update (PUT /api/orders/{id}/)
```json
{
    "items": [
        {
            "id": 5,
            "product": 1,
            "quantity": 3,
            "status": "Delivered"
        },
        {
            "product": 2,
            "quantity": 1,
            "status": "Pending"
        }
    ]
}
```

- id=5 item → gets updated (quantity/status changed).
- A new OrderItem for product=2 → created.
- Transaction ensures both updates are atomic.


> After update (using your OrderSerializer for reading):
```json
{
    "order_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "user": 1,
    "created_at": "2025-10-28T10:20:30Z",
    "items": [
        {
            "product": {
                "id": 1,
                "name": "Phone",
                "price": "500.00",
                "stock": 10,
                "description": "Smartphone"
            },
            "quantity": 3,
            "status": "Delivered"
        },
        {
            "product": {
                "id": 2,
                "name": "Tablet",
                "price": "300.00",
                "stock": 20,
                "description": "Android tablet"
            },
            "quantity": 1,
            "status": "Pending"
        }
    ]
}
```

--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)