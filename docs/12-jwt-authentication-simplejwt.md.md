# Django REST Framework - JWT Authentication with djangorestframework-simplejwt
**Date:** 26 October 2025  
 
---
 
# Django REST Framework Notes

## 1. Authentication

**Official Documentation:**   [Authentication - DRF](https://www.django-rest-framework.org/api-guide/authentication/)  
> Django REST Framework provides various authentication schemes to identify the user making a request.

### 2. JWT Token Decode

**Official Tool:**   [jwt.io](https://www.jwt.io/)  
> JWT (JSON Web Token) can be decoded using this online tool to inspect payloads, header, and signature.

 
### 3. Explanation Video

**Video Tutorial (My Channel - anCoder):**   [JWT Authentication](https://youtu.be/DVKC9VdD_Zg?si=I5idBX4WeMmkg0M9)  

> This video explains how JWT authentication works in Django REST Framework.

 

<br>
<br>

---

## JWT - Json Web Token Authentication 

### Installation Code
```shell
pip install djangorestframework-simplejwt
```


### In your settings.py:

**1. Add app to INSTALLED_APPS**
```py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
]
```

**2. Configure REST Framework authentication**
```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

```

**3. Add token URL patterns**

> In your urls.py (usually project/urls.py):

```py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```