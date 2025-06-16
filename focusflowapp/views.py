from rest_framework import viewsets
from .models import Habit, HabitEntry
from .serializers import HabitSerializer, HabitEntrySerializer, LoginSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class HabitViewSet(viewsets.ModelViewSet):
    """
     API endpoint that allows habits to be viewed or edited.
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['created_at', 'name']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

class HabitEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows habit entries to be viewed or edited.
    """

    queryset = HabitEntry.objects.all()
    serializer_class = HabitEntrySerializer
    ordering = ['-date', 'id']

    def get_queryset(self):
        return HabitEntry.objects.filter(habit__user=self.request.user)


class TokenLoginView(APIView):
    """
    API endpoint for obtaining authentication tokens.
    """
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)