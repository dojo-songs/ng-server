from django.db import models
from ..users.models import User
import re
import bcrypt


email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class SongManager(models.Manager):
    def addSongValidation(self, postData):
        errors = {}

        if len(postData['title']) < 2:
            errors['title']= "Title must be at least 2 characters long"
        if len(postData['artist']) < 2:
            errors['artist'] = "Artist name nust be at least 2 characters long"
        return errors


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name = "songs", on_delete=models.CASCADE)
    numAdded = models.ManyToManyField(User, related_name = "users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)




