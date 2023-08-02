from rest_framework.permissions import BasePermission


class MyBookingPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True
        
        if user.is_authenticated:
            return request.method in ["GET", "HEAD", "OPTIONS"]
        
        else:
            return False



    def has_object_permission(self, request, view, obj):
        pass