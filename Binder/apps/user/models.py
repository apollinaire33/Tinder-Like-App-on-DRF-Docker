from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import m2m_changed
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    class Subscription(models.TextChoices):
        BASE = "20 swipes per day, 10 km"
        VIP = "100 swipes per day, 25 km"
        PREMIUM = "unlimited swipes, dynamic km"

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, default='')
    liked = models.ManyToManyField('self', blank=True, related_name='liked_users', symmetrical=False)
    matched = models.ManyToManyField('self', blank=True, related_name='matched_users')
    subscription = models.CharField(max_length=50, choices=Subscription.choices, default='BASE')
    avatar = models.URLField(max_length=300, null=True, blank=True, default='')
    adress = models.CharField(max_length=255, null=True, blank=True, default='')
    location = models.PointField(null=True, blank=True, default='')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


# django signal for making users matched if they liked each other
@receiver(m2m_changed, sender=UserAccount.liked.through)
def create_chat(sender, instance, action, **kwargs):
    if action == 'post_add':
        liked_users_list = instance.liked.all()
        for liked_user in liked_users_list:
            if instance in liked_user.liked.all():
                liked_user.matched.add(instance)