# Django REST Framework -  API Is_Staff Permissions
**Date:** 28 October 2025  
 
---
> often need to restrict data access so that only `admin (staff)` users can view or manage all records, while normal users can only view their own data.
 
### Useful Resources 
 
**Practice Code** : [Implement is_staff API permission classes in ViewSets](https://github.com/anmamun0/drf-practice-BugBytes/commit/62849e69b9236f8c4cd7e3d8fd5fb21ddcbfedb3) <br> 
 
 
---

<br>
<br>
  
### `is_staff` — in the User model to easily identify admin users.


```py
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        #  Only staff can view all orders, normal users see only their own
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

```