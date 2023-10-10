from rest_framework import serializers
from .models import UserProfile, Order, Attachment


class UserProfileSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'phone_number', 'birth_date', 'password', 'age', 'profile_image')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserProfile(**validated_data)
        user.set_password(password)
        user.save()
        return user


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


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = UserProfile.USERNAME_FIELD

    def validate(self, attrs):
        self.user = self.user_authenticate(phone_number=attrs[self.username_field], password=attrs['password'])
        if self.user is None:
            raise serializers.ValidationError('Неверные учетные данные')
        return super().validate(attrs)

    def user_authenticate(self, phone_number, password):
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except UserProfile.DoesNotExist:
            return None


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
