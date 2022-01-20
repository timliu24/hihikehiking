from distutils.command.upload import upload
from django.db import models
from datetime import datetime, date
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must enter an valid email."
        users_with_email = User.objects.filter(email=postData['email'])
        if len(users_with_email) >= 1:
            errors['email'] = "Email already registered."
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['match'] = "Password does not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class HikeManager(models.Manager):
    def hike_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Title must consist of at least 3 characters."
        if len(postData['location']) < 3:
            errors['location'] = "Location must consist of at least 3 characters."
        if len(postData['time']) < 5:
            errors['time'] = "Time must consist of at least 5 characters."
        if len(postData['meeting']) < 3:
            errors['meeting'] = "Meeting place must consist of at least 10 characters."
        if len(postData['description']) < 10:
            errors['description'] = "Description must consist of at least 10 characters."
        if len(postData['length']) < 1:
            errors['length'] = "Must enter length."
        return errors

class Hike(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()
    time = models.CharField(max_length=5)
    ampm = models.CharField(max_length=2)
    meeting = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=255)
    length = models.CharField(max_length=6)
    image = models.URLField()
    creator = models.ForeignKey(User, related_name="has_posted_hike", on_delete=models.CASCADE)
    added_by = models.ManyToManyField(User, related_name="added_hikes")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = HikeManager()
