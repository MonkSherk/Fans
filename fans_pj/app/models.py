from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    card_number = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    header = models.ImageField(upload_to='headers/', blank=True, null=True)
    is_private = models.BooleanField(default=False)

    # Добавляем поле 'following' для подписок
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='posts/', blank=True, null=True)
    video = models.FileField(upload_to='posts/', blank=True, null=True)
    description = models.TextField()
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.description[:50]}...'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:50]}...'

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    subscription = models.BooleanField(default=False)
    card_number = models.CharField(max_length=16)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount} - {self.created_at}'
