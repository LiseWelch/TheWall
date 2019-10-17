from django.db import models
from datetime import datetime
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user = User.objects.filter(email=postData['email'])
        if len(user) != 0:
            errors['not_unique'] = "User with this e-mail already exist"
            return errors
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name needs to be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name needs to be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = ("Invalid e-mail address")
        if len(postData['password']) < 8:
            errors["password"] = "Password needs to be at least 8 characters long"
        if postData['password']!=postData['confirm']:
            errors["confirm"] = "Passwords do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user_id = models.ForeignKey(User, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.TextField()
    user_id = models.ForeignKey(User, related_name="comments")
    message_id = models.ForeignKey(Message, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)