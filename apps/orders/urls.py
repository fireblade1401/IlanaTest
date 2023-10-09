from django.urls import path
from .views import UserProfileListView, OrderListView, OrderDetailView, register, login

urlpatterns = [
    path('profile/<str:phone_number>/', UserProfileListView.as_view(), name='userprofile-detail'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]
