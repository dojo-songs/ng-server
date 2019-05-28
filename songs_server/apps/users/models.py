from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.

class UserManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long."
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Email address is not valid."     # can change to reg_email if trying to isolate
        if User.objects.filter(email = postData['email']):
            errors['email'] = "Email is already registerd with another account."     # checking to see if email already exists with another account
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match."

        return errors


    def login_validation(self, postData):
        errors = {}
                                # use filter instead of get to get correct response. This call simply checks to see if the email exists within the database.
        result = User.objects.filter(email = postData['email'])

        if result:
                                # grabbing password from index 0 of result dictionary 
            if bcrypt.checkpw(postData['password'].encode(), result[0].password.encode()):
                print("password match")
            else:
                errors['password'] = "Email and password do not match."
        else:
                errors['email'] = "This email has not been registered."     # can change to login_email if trying to isolate

        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
