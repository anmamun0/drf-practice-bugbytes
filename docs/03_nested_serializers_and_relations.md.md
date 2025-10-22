## Django REST Framework- Nested Serializers, SerializerMethodField and Serializer Relations
**Date:** 22 October 2025
 
---


## Overview
In this lesson, we learned advanced serializer concepts in Django REST Framework (DRF)  specifically **Nested Serializers**, **SerializerMethodField**, and **Serializer Relations**. These tools help represent related models and computed fields clearly in API responses.
 
**Official Docs:** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
  
<br>

**1. Nested Serializers**
- You can include one serializer inside another.
- Useful when models are related (Order and OrderItem).
- The many=True parameter is used when there are multiple related objects.
- The read_only=True flag ensures the field is not editable through the API.

<br>
<br>
 
**2. SerializerMethodField**
- Used to add custom or computed fields in the serializer output.
- It’s not part of the model, but generated dynamically through a method.
- The method name should be in the form `get_<field_name>()`.

<br>
<br>

**3. Serializer Relations**
- DRF provides several relation fields to represent related models in different ways.


| Field                     | Description                                                         | Example                                                                    |
| ------------------------- | ------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `PrimaryKeyRelatedField`  | Returns the related object's primary key                            | `order = serializers.PrimaryKeyRelatedField(...)`                          |
| `StringRelatedField`      | Returns the string representation (`__str__`) of the related object | `user = serializers.StringRelatedField()`                                  |
| `SlugRelatedField`        | Returns a specific field (e.g., `name`) instead of ID               | `category = serializers.SlugRelatedField(slug_field='name', queryset=...)` |
| `HyperlinkedRelatedField` | Returns the related object's URL                                    | `url = serializers.HyperlinkedRelatedField(...)`                           |

<br>
<br>

 
 