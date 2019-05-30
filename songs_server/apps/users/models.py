from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your models here.

class UserManager(models.Manager):
    def validate(self, data):
        errors = []
        if len(data['first_name']) <2:
            errors.append('First name must be at least 2 Characters long')
        if len(data['last_name']) <2:
            errors.append('Last name must be at least 2 Characters long')
        if len(data['password'])< 8:
            errors.append('Password must be at least 8 characters Long')
        if not EMAIL_REGEX.match(data["email"]):
            errors.append('Email must be valid!')
        if User.objects.filter(email=data['email']):
            errors.append('Email must be unique')
        if len(data['password']) < 8:
            errors.append("Password must be at least 8 characters long")
        
        return errors

    def easy_create(self, data):
        errors = []
        matching_users = User.objects.filter(email=data['email'])
        if matching_users:
            errors.append('Email aready in use')
            return errors
        hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        return User.objects.create(
            first_name=data["first_name"],
            last_name=data['last_name'],
            email=data['email'],
            password=hashed.decode('utf-8'),
        )

    def login(self, data):
        matching_users = User.objects.filter(email=data['email'])
        if matching_users:
            user = matching_users[0]
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return (True, user)
        return(False, ['Email or Password are Incorrect'])

    def get_user_playlist(self, data):
        user = User.objects.get(id=data['user_id'])
        data = {
            'user_id': user.id,
            'user_first': user.first_name,
            'user_last': user.last_name,
            'songs': [

            ]
        }
        playlist = Playlist.objects.filter(user=user.id)
        if playlist:
            for entry in playlist:
                song = Song.objects.get(id=entry.song.id)
                song_obj = {
                    'song_artist': song.artist,
                    'song_title': song.title,
                    'count': entry.count
                }
                data['songs'].append(song_obj)
        return data


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class SongManager(models.Manager):
    def addSongValidation(self, postData):
        errors = {}

        if len(postData['title']) < 2:
            errors['title']= "Title must be at least 2 characters long"
        if len(postData['artist']) < 2:
            errors['artist'] = "Artist name nust be at least 2 characters long"
        return errors
        
    def easy_create(self, postData):
        return Song.objects.create(
            title=postData['title'],
            artist=postData['artist']
        )
    def get_all_songs(self):
        song_list = Song.objects.all()
        data = {
            'songs': []
        }
        if song_list:
            for song in song_list:
                song_obj = {
                    'id': song.id,
                    'song_artist': song.artist,
                    'song_title': song.title,
                    'count': 0
                }
                playlists = Playlist.objects.filter(song=song.id)
                if playlists:
                    count = 0
                    for entry in playlists:
                        count = count + entry.count
                    song_obj['count'] = count
                data['songs'].append(song_obj)
        return data


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    numAdded = models.ManyToManyField(User, related_name = "users")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = SongManager()

class PlaylistManager(models.Manager):
    def easy_create(self, data):
        try:
            playlist = Playlist.objects.get(song=Song.objects.get(id=data['song_id']), user=User.objects.get(id=data['user_id']))
        except Playlist.DoesNotExist:
            playlist = None
        print('testing.................')
        print(playlist)
        if playlist:
            print('found playlist')
            playlist.count = playlist.count + 1
            playlist.save()
            return playlist
        else:
            return Playlist.objects.create(song=Song.objects.get(id=data['song_id']), user=User.objects.get(id=data['user_id']), count=1)

    def get_song_details(self, data):
        song_info = Playlist.objects.filter(song=data['song_id'])
        song = Song.objects.get(id=data['song_id'])
        data = {
            'song_id': song.id,
            'song_title': song.title,
            'song_artist': song.artist,
            'users': []
        }
        if(song_info):
            for entry in song_info:
                user = User.objects.get(id=entry.user_id)
                user_obj = {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'count': entry.count
                }
                data['users'].append(user_obj)
        return data

class Playlist(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField()
    objects = PlaylistManager()
