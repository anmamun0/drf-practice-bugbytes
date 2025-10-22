## Django REST Framework - Serializers & Response Objects | Browsable API
**Date:** 22 October 2025
 
---


## Overview
This note covers the key concepts from the video on Django REST Framework (DRF), focusing on **serializers**, **response objects**, **URL routing**, and the **Browsable API**. These are essential for building RESTful APIs in Django applications.

**Official Docs:** [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
  
<br>

**1. URL Routing in DRF** 
- API endpoints are defined using Django's `urlpatterns`.
- Separate endpoints for lists of items and single item details.
- Example: `/products/` for all products, `/products/<id>/` for a single product.

<br>
<br>

**2. Serializers** 
- Serializers convert Django models into JSON and vice versa.
- `ModelSerializer` makes it easy to map model fields to JSON.
- You can control which fields are included in the output.
- Supports validation:
  - Field-level validation ensures individual fields meet rules (e.g., price > 0).
  - Object-level validation can enforce rules across multiple fields.

<br>
<br>

**3. Views & Response Objects** 
- `@api_view` decorator is used for function-based API views.
- `Response` object is used instead of Django’s default HttpResponse to return JSON data.
- List views return all objects; detail views return a single object.
- `get_object_or_404` handles non-existing objects gracefully.
- Browsable API allows you to test endpoints directly in the browser.

<br>
<br>

 
 