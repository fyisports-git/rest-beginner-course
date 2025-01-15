"""
Handling permission for handling User profile
"""

from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to access their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user has permission to access the profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UpdateOwnFeed(permissions.BasePermission):
    """Allow users to update their own feed"""

    def has_object_permission(self, request, view, obj):
        """check that user is updating their own feed"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
