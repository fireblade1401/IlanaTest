from rest_framework import serializers
from .models import UserProfile, Order, Attachment


class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'phone_number', 'birth_date', 'password', 'age', 'profile_image')
        read_only_fields = ('phone_number',)


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'file')


class OrderSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'order_number', 'status', 'attachments')

    def create(self, validated_data):
        attachments_data = self.context['request'].FILES
        order = Order.objects.create(**validated_data)

        for attachment in attachments_data.values():
            Attachment.objects.create(order=order, file=attachment)

        return order
