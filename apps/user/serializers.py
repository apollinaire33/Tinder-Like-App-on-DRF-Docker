from django.contrib.auth import get_user_model
from rest_framework import serializers
from geocoder.api import distance

from user.services import UserValidation

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        UserValidation.password_length(password)
        user_obj = User(**validated_data)
        user_obj.set_password(password)
        user_obj.save()
        return user_obj


class UserSerializer(serializers.ModelSerializer):
    distance = serializers.DecimalField(source='distance.km', max_digits=10,
                                        decimal_places=2, required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'description', 'liked', 'matched',
                  'subscription', 'avatar', 'adress', 'location', 'distance')
        read_only_fields = ('location', 'matched')

    
class UserListSerializer(serializers.ModelSerializer):
    distance = serializers.DecimalField(source='distance.km', max_digits=10,
                                        decimal_places=2, required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'description', 'avatar', 'adress', 'location', 'distance')
        read_only_fields = ('location',)

