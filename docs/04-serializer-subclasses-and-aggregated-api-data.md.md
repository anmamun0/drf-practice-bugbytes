 # Django REST Framework - Serializer Subclasses & Aggregated API Data
**Date:** 23 October 2025  
 
---
 
## Overview
In this lesson, I learned how to combine **serialized model data** with **aggregated information** (like counts and max values) in a single API response. This helps create a **summary-style API** — one that gives both detailed objects and useful analytics together.

**Official Docs:** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
  
<br>

 
### 1. ModelSerializer Creation
- A `ProductSerializer` was created using `serializers.ModelSerializer`.
- It automatically handled model fields (`id`, `name`, `price`, `stock`).
- A custom field validator `validate_price()` ensured that the price must be greater than 0.

<br>
<br>

### 2. Custom Serializer for Aggregation
- A manual serializer `ProductInfoSerializer` subclassed from `serializers.Serializer`.
- It included:
  - `products`: serialized list of products (`ProductSerializer(many=True)`).
  - `count`: total number of products.
  - `max_price`: highest product price in the database.

```py
from django.db.models import Max
products = Product.objects.all()
print(products.aggregate(max_price = Max('price'))) # return dictionary value
```

```js
Output:
{'max_price': Decimal('500.050000000000')}
```

<br>
<br>

### 3. Combining Model Data & Aggregation in Views
- In the `product_info` API view:
  - All `Product` objects were fetched from the database.
  - Django ORM’s `aggregate(Max('price'))` found the maximum product price.
  - These values were passed into `ProductInfoSerializer` to build a combined JSON structure.
  - The API returned this structured data using `Response(serializer.data)`.

 
<br>
<br>
