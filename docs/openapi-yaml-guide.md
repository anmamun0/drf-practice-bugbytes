# Django REST Framework - Django + Celery Guide
**Date:** 29 October 2025  
 
---
> YAML stands for "YAML Ain't Markup Language." It is a recursive acronym. Initially, when it was first proposed in 2001, it stood for "Yet Another Markup Language." However, its meaning was changed to "YAML Ain't Markup Language" between December 2001 and April 2002 to emphasize its purpose as a data serialization language rather than a document markup language. 


## Useful Resources Django  
 
 
- **live code editor** : [editor.swagger.io](https://editor.swagger.io/?_gl=1*d1699v*_gcl_au*MTU5NTMyNDY1OS4xNzYyMjUzMDU5) 


<br> 
  
--- 
   
## What is YAML?

`YAML = YAML Ain’t Markup Language`
Used for:
- API documentation (OpenAPI/Swagger)
- Docker & Kubernetes
- GitHub Actions
- CI/CD configs
- Django settings (sometimes)
- YAML = human-friendly JSON


### asic Rules of YAML
<h6>

| Rule        | Explanation          |
| ----------- | -------------------- |
| Indentation | 2 spaces (NO tabs  ) |
| Key: Value  | key followed by `:`  |
| Lists       | use `-`              |
| Strings     | quotes optional      |
| Case        | Case-sensitive       |

</h6>

Key-Value
```yml
name: AN Mamun
role: Backend Engineer
language: Python
```

Numbers, Boolean, Null
```yml
age: 22
is_student: false
experience: null
```

List / Array
```yml
skills:
  - Python
  - Django
  - REST Framework
  - MySQL
```

Nested / Objects
```yml
user:
  name: Mamun
  city: Sylhet
  social:
    github: anmamun0
    linkedin: anmamun0
```

List of Objects
```yml
students:
  - name: Mamun
    id: 101
    cgpa: 3.50
  - name: Rahim
    id: 102
    cgpa: 3.70
```

Same As JSON
```yml
# JSON:
{
  "name": "Mamun",
  "skills": ["Python", "Django"]
}

#  YAML:
name: Mamun
skills:
  - Python
  - Django

```

Comments in YAML
```yml
# This is a comment
name: Mamun  # inline comment allowed
```

YAML for API Example (simple)
```yml
POST /api/login:
  request:
    email: string
    password: string
  response:
    200: success
    400: invalid credentials
```

<br>
<br>

## Format you should follow:

<h6>

| Block                 | Purpose                     |
| --------------------- | --------------------------- |
| `info`                | API meta information        |
| `servers`             | API base URL                |
| `paths`               | All endpoints               |
| `post/get/put/delete` | HTTP methods                |
| `requestBody`         | Input body                  |
| `responses`           | Output responses            |
| `components.schemas`  | Reusable object definitions |


</h6>


```yml
paths:
  /auth/login/:
    post:
      summary: ...
      requestBody:
        ...
      responses:
        ...

components:
  schemas:
    LoginRequest:
      ...
```




## Full Minimal Example

```yml
# Basic OpenAPI YAML Structure

openapi: 3.0.0

info:
  title: TrueLearner API
  version: 1.0.0
  description: Online learning platform API

servers:
  - url: http://localhost:8000/api


# Paths (API Endpoints)
paths:
  /auth/login/:
    post:
      summary: Login user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        "200":
          description: Login successful
        "400":
          description: Invalid credentials

# Components (Schema / Model definitions)
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string

```




<br>

--- 

> [`Author`](https://github.com/anmamun0)
> [`Project`](https://github.com/anmamun0/drf-practice-BugBytes)