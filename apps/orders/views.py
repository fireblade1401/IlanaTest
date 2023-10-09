from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db.models import Q

from .models import UserProfile, Order
from .filters import OrderFilter, UserProfileFilter
from .serializers import UserProfileSerializer, OrderSerializer


class UserProfileListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    filter_class = UserProfileFilter

    def get_queryset(self):
        phone_number = self.kwargs.get('phone_number', None)
        if phone_number:
            return UserProfile.objects.filter(phone_number=phone_number)
        return UserProfile.objects.none()


class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_class = OrderFilter

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(user=user) | Q(user__isnull=True))


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
        'birth_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Birth date'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        'profile_image': openapi.Schema(type=openapi.TYPE_FILE, description='Profile image', format='file'),
    }
)


@swagger_auto_schema(method='post', request_body=request_body)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='Phone number'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
    }
)


@swagger_auto_schema(method='post', request_body=login_request_body)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    phone_number = request.data.get('phone_number', None)
    password = request.data.get('password', None)

    user = UserProfile.objects.filter(phone_number=phone_number).first()

    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
