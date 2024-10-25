from django.contrib import admin

# Register your models here.

from app.models import User, Post, Comment, Payment, Profile

admin.site.register([User,Post,Comment,Payment,Profile])