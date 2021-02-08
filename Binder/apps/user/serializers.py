from django.contrib.auth import get_user_model
from rest_framework import serializers
from geocoder.api import distance
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    distance = serializers.DecimalField(source='distance.km', max_digits=10,
                                        decimal_places=2, required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'description', 'liked', 'matched', 'subscription', 'avatar', 'adress', 'location', 'distance')
        read_only_fields = ('location', 'matched')

    
class UserListSerializer(serializers.ModelSerializer):
    distance = serializers.DecimalField(source='distance.km', max_digits=10,
                                        decimal_places=2, required=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'description', 'avatar', 'adress', 'location', 'distance')
        read_only_fields = ('location',)

