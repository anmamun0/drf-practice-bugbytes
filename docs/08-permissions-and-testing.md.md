# Django REST Framework - DRF Permissions and Testing (tests.py)
**Date:** 25 October 2025  
 
---
 
**Official Docs:** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

## 1. Permissions in DRF

DRF provides a flexible way to control access to API endpoints using **permissions**. Permissions decide whether a user can perform a particular action.

<br>

**Types of Permissions**
- **AllowAny**: Grants access to everyone, authenticated or not.
- **IsAuthenticated**: Only authenticated users can access the endpoint.
- **IsAdminUser**: Only admin users can access.
- **IsAuthenticatedOrReadOnly**: Authenticated users can write; everyone else can read.

<br>

**Custom Permissions**
You can create custom permission classes by extending `BasePermission`:
- Override the `has_permission` and/or `has_object_permission` methods.
- Control access based on user roles, object ownership, or other business logic.

```py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class MyCustomPermission(BasePermission):
    def has_permission(self, request, view):
        # Everyone can access read-only methods (GET, HEAD, OPTIONS)
        return True
         # Only authenticated users can create/update/delete
        if request.user and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed for the owner
        return obj.owner == request.user

# Views.py
class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [MyCustomPermission]

```
> `SAFE_METHODS` "safe," meaning they do not modify resources. read-only methods('GET', 'HEAD', 'OPTIONS') 

**Where it runs:**
- ``has_permission` At the view level, before retrieving any specific object.
- `has_object_permission` Where it runs: At the object level, after retrieving an instance.

<br>

**Applying Permissions**
- Permissions can be applied at the **view level** or **globally** in `settings.py`.
- Example:

```python
  permission_classes = [IsAuthenticated]
```




---

<br>
<br>
<br>
<br>


##  Tesing 

Basic Structure
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




### Run Terminal
```python
python manage.py test
```
