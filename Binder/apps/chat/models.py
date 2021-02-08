from django.db import models
from django.db.models.signals import m2m_changed
from django.utils.timezone import now
from django.dispatch import receiver
from django.core.exceptions import SuspiciousOperation
from user.models import UserAccount


class Chat(models.Model):
    users = models.ManyToManyField(UserAccount, related_name='chats')

    def __str__(self):
        return str(self.id)


# django signal for checking if both users of chat truly matched
@receiver(m2m_changed, sender=Chat.users.through)
def create_chat(sender, instance, action, **kwargs):
    if action == 'post_add':
        users_in_chat = instance.users.all()   
        if len(users_in_chat) >= 3 or len(users_in_chat) < 2:
            Chat.objects.filter(id=instance.id).delete()
        elif len(users_in_chat) == 2:
            user1 = users_in_chat[0]
            user2 = users_in_chat[1]

            user1_mathced_list = user1.matched.all()
            user2_mathced_list = user2.matched.all()

            user_list_for_checking1 = []
            user_list_for_checking2 = []
            for i in user1_mathced_list:
                user_list_for_checking1.append(i)

            for i in user2_mathced_list:
                user_list_for_checking2.append(i)      
            
            if user1 not in user_list_for_checking2 or user2 not in user_list_for_checking1:
                Chat.objects.filter(id=instance.id).delete()


class Messages(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, to_field='email', related_name='messages_by_user', null=True)
    text = models.TextField()
    date = models.DateTimeField(default=now, blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, to_field='id', related_name='messages_in_chat')
    
    def __str__(self):
        return self.text[0:13] + '...'

    # func for checking if message's author in chat
    def save(self, *args, **kwargs): 
        current_chat = self.chat
        if self.user in current_chat.users.all():
            super().save(*args, **kwargs)
        else:
            raise SuspiciousOperation