# Django REST Framework - JWT Refresh Tokens & Authentication
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

## Configure SIMPLE_JWT settings
 
```py
from datetime import timedelta

SIMPLE_JWT = {
    # Lifetime of access token (short-lived)
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),

    # Lifetime of refresh token (long-lived)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    # Token rotation (generate new refresh token when used)
    'ROTATE_REFRESH_TOKENS': True,

    # Blacklist refresh tokens after use
    'BLACKLIST_AFTER_ROTATION': True,

    # Algorithm used to sign JWT
    'ALGORITHM': 'HS256',

    # Secret key for signing JWT
    'SIGNING_KEY': SECRET_KEY,

    # Authentication header type
    'AUTH_HEADER_TYPES': ('Bearer',),

    # If you want custom user claim in JWT payload
    # 'USER_ID_FIELD': 'id',
    # 'USER_ID_CLAIM': 'user_id',
}
```

