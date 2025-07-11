from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Note
from .serializers import NoteSerializer, UserSerializer
from django.db import models

# PUBLIC_INTERFACE
@api_view(['GET'])
def health(request):
    """Health check endpoint."""
    return Response({"message": "Server is up!"})

# PUBLIC_INTERFACE
class RegisterView(generics.CreateAPIView):
    """
    Registration endpoint for new users.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# PUBLIC_INTERFACE
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """
    Login endpoint for users.
    Expects username and password.
    Returns Auth Token on success.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

# PUBLIC_INTERFACE
class NoteListCreateView(generics.ListCreateAPIView):
    """
    List and create notes endpoint. Supports search by title/content via 'search' query param.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        queryset = Note.objects.filter(owner=self.request.user).order_by('-updated_at')
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                models.Q(title__icontains=search_query) |
                models.Q(content__icontains=search_query)
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# PUBLIC_INTERFACE
class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a note owned by the user.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

