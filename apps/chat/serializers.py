from django.contrib.auth import get_user_model
from rest_framework import serializers

from chat.models import Chat, Message

User = get_user_model()


class ChatSerializer(serializers.ModelSerializer):
    messages_in_chat = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'users', 'messages_in_chat')

    def get_messages_in_chat(self, instance):
        messages_in_chat = instance.messages_in_chat.order_by('date')
        return MessageSerializer(messages_in_chat, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ('user', 'text', 'date', 'chat')

    
