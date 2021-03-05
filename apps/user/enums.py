from django.db import models


class Subscription(models.TextChoices):
    BASE = "20 swipes per day, 10 km"
    VIP = "100 swipes per day, 25 km"
    PREMIUM = "unlimited swipes, dynamic km"