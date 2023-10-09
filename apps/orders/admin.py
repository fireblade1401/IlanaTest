from django.contrib import admin
from .models import Order, UserProfile, Attachment
from .tasks import process_order


def set_orders_to_processing(modeladmin, request, queryset):
    for order in queryset:
        process_order.delay(order.id)


set_orders_to_processing.short_description = "Send selected orders to processing"


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status']
    ordering = ['order_number']
    actions = [set_orders_to_processing]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'birth_date',)
    list_filter = ('phone_number', 'birth_date')
    search_fields = ('phone_number', 'birth_date', 'first_name', 'last_name')
    readonly_fields = ('age',)


admin.site.register(Order, OrderAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Attachment)
