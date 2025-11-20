# Django REST Framework - Django Factories
**Date:** 14 November 2025  
 
---
> factory_boy (factories) — a very useful library for creating fake data for Django models (and other ORM models), especially for testing or seeding demo data.
 
--- 


## Summary Cheat Sheet
 
- [1. Meta Class Attributes](#1-meta-class-attributes)
- [2. Factory Field Declarations](#2-factory-field-declarations)
- [3. Fuzzy Helpers (Randomized Values)](#3-fuzzy-helpers-randomized-values)
- [4. Faker vs Fuzzy](#4-faker-vs-fuzzy)
- [5. Lifecycle Hooks & Methods](#5-lifecycle-hooks--methods)
- [6. Factory Creation Methods](#6-factory-creation-methods)


<br>
<br>

### What is factory_boy?

factory_boy is a Python library that helps you easily create test or demo data for your Django (or SQLAlchemy, etc.) models — instead of manually creating instances each time.

It’s often used with:

- Django tests (pytest, unittest)
- Fake data seeding (with Faker)
- Model relationships (ForeignKey, ManyToMany)
- Randomized, realistic data generation


Installation 
 
```shell
pip install factory-boy faker
```
- `factory-boy` → creates models
- `faker` → generates realistic fake data (name, email, date, etc.)

 
---
 
## 1. Meta Class Attributes 

[Home](#summary-cheat-sheet) These control how the factory behaves internally.

<h6>

| Attribute                    | Type        | Description                                                 |
| ---------------------------- | ----------- | ----------------------------------------------------------- |
| **model**                    | Model class | Specifies which model the factory builds/creates            |
| **strategy**                 | Constant `factory.CREATE_STRATEGY` / `factory.BUILD_STRATEGY` / `factory.STUB_STRATEGY` | Default creation behavior (create/build/stub) |
| **abstract**                 | bool        | Marks as abstract (base factory)                            |
| **exclude**                  | list/tuple  | Fields to skip from initialization                          |
| **django_get_or_create**     | list/tuple  | Fields to use for `get_or_create()`                         |
| **inline_args**              | list/tuple  | Fields that can be given positionally                       |
| **rename**                   | dict        | Maps input field names to model field names                 |
| **skip_postgeneration_save** | bool        | Don’t save after post-generation hooks                      |
| **parameters**               | dict        | Default parameters for the factory                          |
| **model_class**              | alias       | (Internally same as `model`)                                |
| **base_factory**             | factory     | For inherited factories                                     |

</h6>



```py
import factory
from factory import fuzzy
from faker import Faker
from datetime import datetime
from .models import Product, Category, User

fake = Faker()

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        strategy = factory.CREATE_STRATEGY  # Create & save to DB
        abstract = False                    # Concrete factory
        exclude = ('temp_field',)           # Not passed to model
        django_get_or_create = ('name', 'seller')  # Avoid duplicates
        inline_args = ('name', 'price')     # Allows positional args
        rename = {'desc': 'description'}    # Custom field rename
        skip_postgeneration_save = False    # Keep default saving

    # === Fields ===
    category = factory.SubFactory('apps.shop.factories.CategoryFactory')
    seller = factory.SubFactory('apps.shop.factories.UserFactory', is_seller=True)
    name = factory.Sequence(lambda n: f"Product {n}")
    price = fuzzy.FuzzyDecimal(10.0, 1000.0)
    stock = fuzzy.FuzzyInteger(1, 50)
    description = factory.Faker('sentence')
    created_at = factory.LazyFunction(datetime.now)
    is_active = factory.Iterator([True, True, False])
    temp_field = factory.LazyFunction(lambda: fake.word())  # excluded from save 
```
   
If your `Meta.inline_args = ('name', 'price')`, 
you can use positional arguments:
```py
ProductFactory("Laptop", 999.99)
```

If your `Meta.rename = {'desc': 'description'}`,
you can use:
```py
ProductFactory(desc="Nice product")
```

<br>
<br>








## 2. Factory Field Declarations

[Home](#summary-cheat-sheet) Each attribute of your factory defines how to generate a field value.


Field Types / Declarations
- `Faker(provider, **kwargs)` — generate realistic fake data
- `Sequence(lambda n: ...)` — unique sequential values
- `LazyAttribute(lambda obj: ...)` — compute value based on other fields
- `LazyFunction(func)` — call a function to generate value
- `SelfAttribute("field_name")` — copy value from another field
- `Iterator(list_or_generator)` — cycle through list or choices
- `Dict({key: value, ...}) `— generate a dictionary field
- `List([value1, value2, ...])` — generate a list field
- `SubFactory(OtherFactory)` — create related object (FK / O2O)
- `RelatedFactory(OtherFactory, related_name)` — create reverse relation object
- `Trait(...) (inside class Params)` — predefined set of field values

<h6>

| Field Helper                        | Description                        | Example              |
| ----------------------------------- | ---------------------------------- | -------------------- |
| **factory.Faker()**                 | Fake data from `Faker`             | `factory.Faker('email')`  |
| **factory.Sequence()**              | Incremental numbers            | `factory.Sequence(lambda n: f"user{n}")` |
| **factory.LazyAttribute()**         | Computed from other fields   | `factory.LazyAttribute(lambda o: o.first_name + ' ' + o.last_name)` |
| **factory.LazyFunction()**          | Evaluates function each time   | `factory.LazyFunction(uuid.uuid4)`   |
| **factory.Iterator()**              | Cycles values                  | `factory.Iterator(['A', 'B', 'C'])` |
| **factory.Trait()**                 | Conditional presets,  — Reusable Configurations        | See below  |
| **factory.SubFactory()**            | Creates related model          | `factory.SubFactory(UserFactory)`  |
| **factory.RelatedFactory()**        | Creates related model in reverse (OneToOne) | `factory.RelatedFactory(ProfileFactory, 'user')`  |
| **factory.SelfAttribute()**         | Copy value from another field  | `factory.SelfAttribute('user.email')`|
| **factory.Dict()**                  | Generates dictionary           | `factory.Dict({'key': 'value'})`     |
| **factory.Maybe()**                 | Conditional logic              | `factory.Maybe('is_active', 'yes', 'no')`|
| **factory.LazyAttributeSequence()** | Lazy + sequence combined  | `factory.LazyAttributeSequence(lambda o, n: f"{o.category}-{n}")` |


Methods Used in Relationships

| Method                           | Description                                        |
| -------------------------------- | -------------------------------------------------- |
| **factory.SubFactory()**         | Creates a related model automatically (ForeignKey) |
| **factory.RelatedFactory()**     | Creates model in reverse direction (OneToOne)      |
| **factory.RelatedFactoryList()** | Creates a list of related models                   |
| **factory.post_generation**      | For ManyToMany or extra setup after save           |
 
</h6>




```py
# models.py
from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100)

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    join_date = models.DateField()
    rating = models.FloatField(default=0.0)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('banned', 'Banned')
    ])

```
```py
# factories.py
import factory
from factory import fuzzy
from datetime import datetime
from .models import User, Country

# -------------------------------
# Country Factory
# -------------------------------
class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country
        django_get_or_create = ("name",)

    # Faker directly from factory
    name = factory.Faker("country")


# -------------------------------
# User Factory (ALL declarations)
# -------------------------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    # 1. Sequence — unique values
    username = factory.Sequence(lambda n: f"user_{n}")

    # 2. factory.Faker — realistic text data
    email = factory.Faker("email")
    bio = factory.Faker("paragraph", nb_sentences=3)

    # 3. SubFactory — related object
    country = factory.SubFactory(CountryFactory)

    # 4. fuzzy — numeric/date ranges
    age = fuzzy.FuzzyInteger(18, 65)
    rating = fuzzy.FuzzyFloat(0.0, 5.0, precision=1)
    join_date = fuzzy.FuzzyDate(datetime(2020, 1, 1).date(), datetime(2025, 12, 31).date())

    # 5. Iterator — fixed choices
    status = factory.Iterator(["active", "pending", "banned"])

    # 6. LazyAttribute — depends on other fields
    is_active = factory.LazyAttribute(lambda o: o.status == "active")

    # 7. SelfAttribute — copy value
    email_alias = factory.SelfAttribute("email")

    # 8. LazyFunction — runs any function
    random_code = factory.LazyFunction(lambda: f"USR-{factory.random.re.random_number(digits=5)}")

    # 9. Traits — preset variations
    class Params:
        # Trait: active user
        active_user = factory.Trait(status="active",is_active=True)
        # Trait: banned user
        banned_user = factory.Trait(status="banned",is_active=False)
        # Trait: teenage user
        teen_user = factory.Trait(age=fuzzy.FuzzyInteger(13, 19))

```
 

```py
# Normal user
user1 = UserFactory()
print(user1.username, user1.status, user1.is_active, user1.age, user1.email, user1.country.name)

# Active user trait
active_user = UserFactory(active_user=True)
print(active_user.username, active_user.status, active_user.is_active)

# Banned user trait
banned_user = UserFactory(banned_user=True)
print(banned_user.username, banned_user.status, banned_user.is_active)

# Teen user trait
teen_user = UserFactory(teen_user=True)
print(teen_user.username, teen_user.age)

# Combine traits
teen_active = UserFactory(teen_user=True, active_user=True)
print(teen_active.username, teen_active.age, teen_active.status, teen_active.is_active)

# Create batch
users = UserFactory.create_batch(5)
for u in users:
    print(u.username, u.status, u.age, u.country.name)
```

<br>








## 3. Fuzzy Helpers (Randomized Values)
[Home](#summary-cheat-sheet) Fuzzy classes generate randomized data without Faker. `from factory import fuzzy`

Fuzzy Field Types / Helpers
- `FuzzyInteger(low, high)` — random integer in range
- `FuzzyDecimal(low, high, precision=2)` — random decimal
- `FuzzyFloat(low, high, precision=2)` — random float
- `FuzzyText(length, prefix="", chars=None)` — random string
- `FuzzyChoice([list])` — random choice from list
- `FuzzyDate(start_date, end_date)` — random date in range
- `FuzzyDateTime(start_datetime, end_datetime)` — random datetime in range

<h6>

| Fuzzy Field                         | Description                  | Example                                               |
| ----------------------------------- | ---------------------------- | ----------------------------------------------------- |
| **fuzzy.FuzzyInteger(a, b)**        | Random integer between a & b | `fuzzy.FuzzyInteger(10, 100)`                         |
| **fuzzy.FuzzyDecimal(a, b)**        | Random decimal between a & b | `fuzzy.FuzzyDecimal(10.5, 999.9)`                     |
| **fuzzy.FuzzyText(length)**         | Random text                  | `fuzzy.FuzzyText(length=12, prefix="Prod_")`         |
| **fuzzy.FuzzyChoice(choices)**      | Randomly picks one choice    | `fuzzy.FuzzyChoice(['A', 'B'])`                       |
| **fuzzy.FuzzyDate(start, end)**     | Random date                  | `fuzzy.FuzzyDate(date(2020,1,1))`                     |
| **fuzzy.FuzzyDateTime(start, end)** | Random datetime              | `fuzzy.FuzzyDateTime(datetime.now())`                 |
| **fuzzy.FuzzyAttribute(function)**  | Random custom value          | `fuzzy.FuzzyAttribute(lambda: random.randint(1,100))` |

</h6>

Faker Common Providers
```py
name = factory.Faker('name')
first_name = factory.Faker('first_name')
last_name = factory.Faker('last_name')
```

<h6>

| Category            | Faker Provider                         | Example Output                                    |
| ------------------- | -------------------------------------- | ------------------------------------------------- |
| **Person**          | `'name'`                               | "Mamun Rahman"                                    |
|                     | `'first_name'`, `'last_name'`          | "Mamun", "Rahman"                                 |
|                     | `'user_name'`                          | "mamun007"                                        |
|                     | `'job'`                                | "Software Engineer"                               |
| **Internet**        | `'email'`                              | "[mamun@example.com](mailto:mamun@example.com)"   |
|                     | `'domain_name'`                        | "google.com"                                      |
|                     | `'ipv4'`, `'ipv6'`                     | "192.168.0.1"                                     |
|                     | `'url'`                                | "[https://django.dev](https://django.dev)"        |
|                     | `'uri'`                                | "/home/products"                                  |
|                     | `'slug'`                               | "cool-product"                                    |
| **Text**            | `'sentence'`                           | "This is a fake sentence."                        |
|                     | `'paragraph'`                          | "Lorem ipsum dolor sit amet..."                   |
|                     | `'text'`                               | "Generated random text..."                        |
| **Numbers**         | `'random_int'`                         | 57                                                |
|                     | `'pyint'`, `'pyfloat'`, `'pydecimal'`  | 42.5                                              |
|                     | `'random_number'`                      | 873291                                            |
| **Address**         | `'city'`                               | "Sylhet"                                          |
|                     | `'street_address'`                     | "123 Main St"                                     |
|                     | `'postcode'`                           | "3100"                                            |
|                     | `'country'`                            | "Bangladesh"                                      |
| **Date & Time**     | `'date'`                               | "2025-11-13"                                      |
|                     | `'time'`                               | "10:22:54"                                        |
|                     | `'date_time'`                          | "2024-06-15 09:30:00"                             |
|                     | `'month'`, `'year'`                    | "07", "2025"                                      |
|                     | `'day_of_week'`                        | "Monday"                                          |
|                     | `'future_datetime'`, `'past_datetime'` | dynamic datetimes                                 |
| **Company**         | `'company'`                            | "MamunSoft Ltd."                                  |
|                     | `'company_email'`                      | "[info@mamunsoft.com](mailto:info@mamunsoft.com)" |
|                     | `'catch_phrase'`                       | "Smart scalable web solutions"                    |
| **Phone & Contact** | `'phone_number'`                       | "+880 1723 456789"                                |
|                     | `'msisdn'`                             | "8801712345678"                                   |
| **Commerce**        | `'color_name'`                         | "Sky Blue"                                        |
|                     | `'currency_code'`                      | "USD"                                             |
|                     | `'ean13'`                              | "1234567890123"                                   |
| **Miscellaneous**   | `'uuid4'`                              | "e6b9a5a2-ff84-4a15-9058-5583a0e62a6f"            |
|                     | `'boolean'`                            | True / False                                      |
|                     | `'file_name'`                          | "invoice.pdf"                                     |
|                     | `'mime_type'`                          | "image/png"                                       |
|                     | `'language_name'`                      | "English"                                         |
|                     | `'word'`, `'words'`                    | "banana", ["red", "car", "happy"]                 |
|                     | `'binary'`                             | b'\x00\x01...'                                    |

</h6>

Faker with Parameters (Advanced Usage)
```py
factory.Faker('date_time_between', start_date='-1y', end_date='now')
factory.Faker('word', ext_word_list=['Django', 'Python', 'React'])
factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
factory.Faker('text', max_nb_chars=100)
factory.Faker('date_of_birth', minimum_age=20, maximum_age=60)
factory.Faker('color_name')
```

<br>
<br>
















## 4. Faker vs Fuzzy
[Home](#summary-cheat-sheet) `from factory import Faker ,fuzzy`  When to Use Which
<h6>


| Case                                           | Use Faker                        | Use Fuzzy               |
| ---------------------------------------------- | -------------------------------- | ----------------------- |
| You want *realistic text, names, emails, etc.* | ✅ Yes                            | ❌ No                    |
| You want *controlled numeric range (min, max)* | ❌ No                             | ✅ Yes                   |
| You want *custom logic*                        | Combine Faker + LazyAttribute | FuzzyAttribute       |
| You want *human-like sentences*                | ✅ Yes                            | ❌ No                    |
| You want *random price between 10–500*         | ❌                                | ✅ FuzzyDecimal(10, 500) |
| You want *city, company, email*                | ✅ Faker                          | ❌ Fuzzy                 |

</h6>

<br>
<br>















## 5. Lifecycle Hooks & Methods
[Home](#summary-cheat-sheet) Hooks run before or after creation.

- `@lazy_attribute` — compute value based on other fields
- `@post_generation` — custom actions after object creation

<h6>

| Hook                                     | When it runs                            | Use Case                     |
| ---------------------------------------- | --------------------------------------- | ---------------------------- |
| **@factory.post_generation**             | After instance creation                 | For ManyToMany, related data |
| **@factory.lazy_attribute**              | At runtime, per instance                | Dynamically computed value   |
| **@factory.lazy_attribute_sequence**     | Combines lazy + sequence                | e.g. unique slugs            |
| **@factory.post_generation_method_call** | Calls a method on model after create    | Common for `set_password`    |
| **_adjust_kwargs()**                     | Internal, used to pre-process arguments |                              |

</h6>     


```py
Example — Post Generation
@factory.post_generation
def tags(self, create, extracted, **kwargs):
    if not create:
        return
    if extracted:
        for tag in extracted:
            self.tags.add(tag)
```
 





<br>
<br>







## 6. Factory Creation Methods 
[Home](#summary-cheat-sheet) 

<h6>

| Usage           | Code                                   | Description        |
| --------------- | -------------------------------------- | ------------------ |
| Create one      | `ProductFactory()`                     | Saves to DB        |
| Create many     | `ProductFactory.create_batch(10)`      | Creates 10 , Creates `n` objects and saves          |
| Build (unsaved) | `ProductFactory.build()`               | Doesn’t touch DB   |
| Build many      | `ProductFactory.build_batch(5)`        | Unsaved list       |
| Stub            | `ProductFactory.stub()`                | Mock-like object   |
| Positional args | `ProductFactory("Phone", 500)`         | Uses `inline_args` |
| ManyToMany      | `ProductFactory(tags=["Sale", "Hot"])` | post_generation    |
| SubFactory      | auto creates FK parent                 | Linked models      |
| RelatedFactory  | auto creates child                     | Reverse relation   |
 
</h6>

```py
# Saves to DB
product = ProductFactory.create(name="Car")

# Doesn’t save
unsaved_product = ProductFactory.build(name="Table")

# Lightweight dummy
stub = ProductFactory.stub()
print(stub.name)
print(stub.pk)  # None

```
 













<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>



 
## Example 
 
> models.py
```py
from django.db import models
from django.contrib.auth.models import AbstractUser


# --------------------------
#  USER MODEL
# --------------------------
class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    def __str__(self):
        return self.username


# --------------------------
#  CATEGORY MODEL
# --------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# --------------------------
#  PRODUCT MODEL
# --------------------------
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.price}"


# --------------------------
#  ORDER MODEL
# --------------------------
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"


# --------------------------
#  ORDER ITEM MODEL
# --------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


# --------------------------
#  REVIEW MODEL
# --------------------------
class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} ({self.rating}⭐)"


```

> factories.py
```py
import random
import factory
from faker import Faker
from factory import fuzzy
from datetime import datetime, timedelta

from .models import User, Category, Product, Order, OrderItem, Review

fake = Faker()


# --------------------------
#  USER FACTORY
# --------------------------
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    phone = factory.Faker("phone_number")
    is_seller = factory.Iterator([True, False])
    is_customer = factory.LazyAttribute(lambda o: not o.is_seller)
    password = factory.PostGenerationMethodCall("set_password", "123456")
 
# --------------------------
#  CATEGORY FACTORY
# --------------------------
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    description = factory.Faker("sentence")
 
# --------------------------
#  PRODUCT FACTORY
# --------------------------
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    seller = factory.SubFactory(UserFactory, is_seller=True)
    name = factory.Faker("sentence", nb_words=3)
    price = fuzzy.FuzzyDecimal(10.0, 1000.0)
    stock = fuzzy.FuzzyInteger(0, 100)
    created_at = factory.LazyFunction(datetime.now)
    is_active = factory.Iterator([True, True, False])  # 2/3 active
 
# --------------------------
#  ORDER FACTORY
# --------------------------
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(UserFactory, is_customer=True)
    total_price = fuzzy.FuzzyDecimal(50.0, 2000.0)
    status = factory.Iterator(["Pending", "Shipped", "Delivered", "Cancelled"])
    created_at = factory.LazyFunction(datetime.now)

    # post_generation for ManyToMany (through OrderItem)
    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for item in extracted:
                self.items.add(item)
 
# --------------------------
#  ORDER ITEM FACTORY
# --------------------------
class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = fuzzy.FuzzyInteger(1, 5)
    subtotal = factory.LazyAttribute(lambda o: o.product.price * o.quantity)
 
# --------------------------
#  REVIEW FACTORY
# --------------------------
class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    product = factory.SubFactory(ProductFactory)
    user = factory.SubFactory(UserFactory)
    rating = fuzzy.FuzzyInteger(1, 5)
    comment = factory.Faker("sentence")
    created_at = factory.LazyFunction(lambda: datetime.now() - timedelta(days=random.randint(0, 90))) 
```


 



--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)