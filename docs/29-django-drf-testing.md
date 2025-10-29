# Django REST Framework - Django REST Framework (DRF) Tesing 
**Date:** 29 October 2025  
 
---
Throttling is a mechanism to limit the rate of API requests from clients. It helps protect your API from overuse, abuse, or denial-of-service attacks. DRF provides several built-in throttles and allows custom throttling logic.

## Useful Resources Django  
 

- **Testing Guide** : [django-rest-framework.org/api-guide/testing](https://www.django-rest-framework.org/api-guide/testing/)
 
    
**Practice Code** : [Implement Testing APITestCas ](https://github.com/anmamun0/drf-practice-BugBytes/commit/ebab8e261c7b9516c3470b43a81afb159335be9d) <br>  
 
 
--- 
 
 <h6>
 
# Django Test Classes — Full Comparison

| Class                                 | Comes From              | Purpose                      | Used For                                  | Database Support | Example                          |
| ------------------------------------- | ----------------------- | ---------------------------- | ----------------------------------------- | ---------------- | -------------------------------- |
| **`unittest.TestCase`**               | Python Standard Library | Basic Python testing         | Pure Python code, no Django ORM           |  No DB support  | Testing math functions, etc.     |
| **`django.test.SimpleTestCase`**      | Django                  | Lightweight Django test      | Views or functions **without database**   |  No DB          | Test utilities, middleware, etc. |
| **`django.test.TestCase`**            | Django                  | Full Django test class       | Models, views, forms, URLs, etc.          |   Uses test DB   | Unit testing your Django app     |
| **`rest_framework.test.APITestCase`** | Django REST Framework   | Testing APIs (HTTP requests) | REST APIs (GET/POST/PUT/DELETE)           |  Uses test DB   | Testing API endpoints            |
| **`django.test.TransactionTestCase`** | Django                  | Low-level DB test            | Testing **transactions** or **atomicity** |  Full DB access | Testing rollback behavior        |

 </h6>
 
### 1. SimpleTestCase (No Database)

> Used when your test doesn’t need a database — for example, testing middleware or utility functions.
```py
from django.test import SimpleTestCase

class MathTest(SimpleTestCase):
    def test_addition(self):
        self.assertEqual(2 + 3, 5)
```



### 2. TestCase (With Database)

> Used for testing models, views, or any database-related logic.
> Django creates a temporary test database and deletes it after tests finish.
```py
from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Laptop", price=1200)

    def test_product_name(self):
        self.assertEqual(self.product.name, "Laptop")
```    

### 3. APITestCase (For REST APIs)

> Used when testing API endpoints.
> It uses DRF’s APIClient, which supports authentication, headers, tokens, etc.
```py
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

class ProductAPITest(APITestCase):
    def test_get_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

```


### 4. TransactionTestCase (For Transaction Control)
> Used when testing database rollback/commit behavior.
```py 
from django.test import TransactionTestCase
from django.db import transaction

class TransactionExampleTest(TransactionTestCase):
    def test_atomic_block(self):
        with self.assertRaises(Exception):
            with transaction.atomic():
                raise Exception("Simulating rollback")
```


---
<br>
<br>
<br>

##  Basic Structure
```python
from django.test import TestCase
from .models import MyModel

class MyModelTest(TestCase):
    def setUp(self):
        # Setup initial data
        MyModel.objects.create(name="Example")

    def test_model_creation(self):
        obj = MyModel.objects.get(name="Example")
        self.assertEqual(obj.name, "Example")
```
- `TestCase` is the base class for all Django tests.
- `setUp()` runs before each test.
- Test methods must start with `test_`.


```python
from django.test import TestCase
from django.urls import reverse
from .models import Car

class CarModelTest(TestCase):
    # Writing Model Tests
    def test_car_creation(self):
        car = Car.objects.create(name="BMW", price=5000000)
        self.assertEqual(car.name, "BMW")
        self.assertEqual(car.price, 5000000)
        self.assertIsInstance(car, Car)
    # Writing View Tests 
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to my site")

```

### Common Checks Assertions

| Assertion                        | Description                        |
| -------------------------------- | ---------------------------------- |
| `assertEqual(a, b)`              | Checks a == b                      |
| `assertNotEqual(a, b)`           | Checks a != b                      |
| `assertTrue(x)`                  | Checks x is True                   |
| `assertFalse(x)`                 | Checks x is False                  |
| `assertIsInstance(obj, cls)`     | Checks if obj is instance of cls   |
| `assertContains(response, text)` | Checks if response contains text   |
| `assertRedirects(response, url)` | Checks response redirects to a URL |


### Using self.client

`self.client` is a test client that simulates a browser for sending HTTP requests.
It can be used to test `GET`, `POST`, `PUT`, `PATCH`, `DELETE` requests.

| Method                             | Description                         |
| ---------------------------------- | ----------------------------------- |
| `client.get(path, data=None)`      | Sends a GET request                 |
| `client.post(path, data=None)`     | Sends a POST request                |
| `client.put(path, data=None)`      | Sends a PUT request                 |
| `client.patch(path, data=None)`    | Sends a PATCH request               |
| `client.delete(path, data=None)`   | Sends a DELETE request              |
| `client.login(username, password)` | Logs in a test user                 |
| `client.logout()`                  | Logs out the test user              |
| `client.session`                   | Access session data                 |
| `client.cookies`                   | Read/write cookies                  |
| `client.force_login(user)`         | Force login a user without password |



### Test Folder Structure (Recommended)

```shell
myapp/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_serializers.py
│   └── test_api.py
```


### Run Terminal
```python
python manage.py test
```







--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)