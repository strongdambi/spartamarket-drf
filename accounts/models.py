from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDERS = (
        ("male", "male"),
        ("female", "female"),
        ("other", "other"),
    )

    nickname = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
    
    def soft_delete(self):
        self.is_active = False  # is_active False로 만들어 계정 비활성화
        self.save()
        return True
    
    def delete(self, using=None, keep_parents=False):
        self.soft_delete()  # delete()를 사용하게 오버라이딩
        return True
