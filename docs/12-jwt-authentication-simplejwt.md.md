# Django REST Framework - JWT Authentication with djangorestframework-simplejwt
**Date:** 26 October 2025  
 
---
 
**Official Docs:** [cdrf.co/3.11/rest_framework.viewsets/GenericViewSet](https://www.cdrf.co/3.11/rest_framework.viewsets/GenericViewSet.html)

<br>

**Explanation Video:** [JWT Authentication (anCoder)](https://youtu.be/DVKC9VdD_Zg?si=I5idBX4WeMmkg0M9)

JWT - Json Web Token Authentication 

### Installation Code
```shell
pip install djangorestframework-simplejwt
```
<br>


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