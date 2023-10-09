import django_filters
from .models import Order, UserProfile


class OrderFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(field_name="creation_date", lookup_expr='gte')
    max_date = django_filters.DateFilter(field_name="creation_date", lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['status', 'min_date', 'max_date']


class UserProfileFilter(django_filters.FilterSet):
    min_birth_date = django_filters.DateFilter(field_name="birth_date", lookup_expr='gte')
    max_birth_date = django_filters.DateFilter(field_name="birth_date", lookup_expr='lte')

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'min_birth_date', 'max_birth_date']