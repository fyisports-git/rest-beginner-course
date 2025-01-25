"""
Views for this project
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from . import serializers, models, permissions


class HelloAPIView(APIView):
    """Hello API view"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        name = request.query_params.get('name', '')
        an_apiview = [
            'Uses HTTP methods as function(get, post, put, patch, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your application logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': f'Hello!{name}', 'an_apiview': an_apiview})

    def post(self, request):
        """Create a Hello message with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )

    def put(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            return Response({'message': f'New name is {name}'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )

    def patch(self, request, pk=None):
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        return Response({'method': 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """Test Hello API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a Hello message"""
        a_viewset = [
            'Uses action (list, create, retrieve, \
                update, partial_update, delete)',
            'Automatically maps to URLs using Routers',
            'Provides more functionalities with less code',
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new Hello message with name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            return Response({'message': f'Name is {name}'})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )

    def retrieve(self, request, pk=None):
        """Handle getting an object by it's ID"""
        return Response({'method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object by it's ID"""
        return Response({'method': 'UPDATE'})

    def partial_update(self, request, pk=None):
        """Handle partial update of an object by it's ID"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Handle deleting an object by it's ID"""
        return Response({'method': 'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handling accessing, creating and updating User profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name', 'email',)


class UserLoginAPIView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, retrieving and updating profile feed items"""
    serializer_class = serializers.ProfileFeedSerializer
    queryset = models.ProfileFeedItem.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (
        permissions.UpdateOwnFeed,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

    def get_queryset(self):
        """Retrieve feed for authenticated User only"""
        return self.queryset.filter(
            user_profile=self.request.user
            ).order_by('-id')
