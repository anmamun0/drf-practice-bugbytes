# Django REST Framework - Django + Celery Guide
**Date:** 29 October 2025  
 
---
Celery is an asynchronous task queue that allows Django to perform background tasks like sending emails, generating reports, or handling long-running processes.
Redis is commonly used as a message broker and result backend for Celery.


## Useful Resources Django  
 

- **Djoser Doc** : [djoser.readthedocs.io](https://djoser.readthedocs.io/en/latest/getting_started.html)
- **Djoser Github** : [github.com/sunscrapers/djoser](https://github.com/sunscrapers/djoser)

**Practice Code** : [Implement Djoser](https://github.com/anmamun0/drf-practice-BugBytes/commit/ebab8e261c7b9516c3470b43a81afb159335be9d) <br>  
 
  
--- 
  
pip install django-extensions
pip install djangorestframework
pip install django-silk
pip install drf-spectacular
pip install django-filter

pip install django-redis
pip install "redis[hiredis]"
pip install celery
pip install scoop
pip install eventlet

pip install djoser

Extension:
REST Client

Installation
```sh
pip install djoser
```
### 2. Configure REST Framework (with JWT)
```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

### 3. Configure URLs
```py
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('djoser.urls')),           # endpoints: register, user
    path('api/auth/', include('djoser.urls.jwt')),       # JWT endpoints: token, refresh
]
```
### Common Endpoints Provided by Djoser
<h6>

| Endpoint                                  | Method               | Description                  |
| ----------------------------------------- | -------------------- | ---------------------------- |
| `/api/auth/users/`                        | POST                 | User registration            |
| `/api/auth/users/me/`                     | GET                  | Get current user details     |
| `/api/auth/users/<id>/`                   | GET/PUT/PATCH/DELETE | User detail/update/delete    |
| `/api/auth/jwt/create/`                   | POST                 | Obtain JWT token (login)     |
| `/api/auth/jwt/refresh/`                  | POST                 | Refresh JWT token            |
| `/api/auth/jwt/verify/`                   | POST                 | Verify JWT token             |
| `/api/auth/users/set_password/`           | POST                 | Change password              |
| `/api/auth/users/reset_password/`         | POST                 | Request password reset email |
| `/api/auth/users/reset_password_confirm/` | POST                 | Confirm password reset       |

</h6>




--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)