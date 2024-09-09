from django.db import models
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to="images/")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category_products")
    tags = models.ManyToManyField(Tag, blank=True, related_name="tag_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
