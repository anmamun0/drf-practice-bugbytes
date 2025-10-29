# Django REST Framework - ModelSerializer Fields - Best Practices
**Date:** 29 October 2025  
 
---
> A **ModelSerializer** is a shortcut for creating serializers that automatically generate fields and validation rules from your model.

## Useful Resources Django  
 
- **modelserializer :** [django-rest-framework.org/api-guide/serializers/#modelserializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)


**Practice Code** : [Commit Message](https://github.com/anmamun0/drf-practice-BugBytes/commit/8df9ff431ff78d27d6989081a33bcaa49d9c4975) <br>  

  
--- 
<br>


## ModelSerializer Fields  
 
 
Includes default validation (unique, blank, null).
<br>

Explicit Field Definition
- Use `fields = ['id', 'name', 'price']` for control.
- Avoid `fields = '__all__'` in production.

Exclude Fields , to skip specific fields.
```py
exclude = ['created_at'] 
```

Read-only & Write-only Fields
```py
read_only_fields = ['id', 'created_at']
```

extra_kwargs → customize behavior.
```py
extra_kwargs = {
    'password': {'write_only': True},
    'id': {'read_only': True}
}
```

Protect sensitive data with write_only=True. 
Read-only Fields in Meta

```py
read_only_fields = ['id', 'created_at']
```
 
 
--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)