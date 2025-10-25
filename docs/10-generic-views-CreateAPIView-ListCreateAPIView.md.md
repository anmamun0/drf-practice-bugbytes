# Django REST Framework - Generic View CreateAPIView and ListCreateAPIView Internals
**Date:** 25 October 2025  
 
---
 
**Official Docs:** [cdrf.co/3.11/rest_framework.viewsets/GenericViewSet](https://www.cdrf.co/3.11/rest_framework.viewsets/GenericViewSet.html)

In Django REST Framework (DRF), Generic Views simplify `CRUD` operations by combining mixins with `GenericAPIView`.

They provide built-in functionality for creating, `listing`, `updating`, and `deleting `model instances — without writing repetitive code.

<br>
   
### CreateAPIView
Used to handle HTTP `POST` requests for creating new model instances.


### ListCreateAPIView
 
Used to handle both `GET` and `POST` requests — listing objects and creating new ones.

*Mixins Used:* <br>
`ListModelMixin` and `CreateModelMixin`