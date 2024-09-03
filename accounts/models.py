from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDERS = (
        ("male", "male"),
        ("female", "female"),
        ("other", "other"),
    )

    name = models.CharField(max_length=50, blank=True)
    nickname = models.CharField(max_length=50, blank=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=GENDERS)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
