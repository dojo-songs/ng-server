from django.shortcuts import HttpResponse
from .models import *


from django.core import serializers
import json


def show(req, user_id):
    user = User.objects.filter(id=user_id)
    json_user = serializers.serialize('json', user)
    return HttpResponse(json_user, status=200, content_type='application/json')

def create(req):
    post_data = json.loads(req.body.decode())
    errors = User.objects.validate(post_data)
    if errors:
        return HttpResponse(json.dumps(errors), status=400, content_type='application/json')
    entire_user = User.objects.easy_create(post_data)
    
    user = {
        'first_name': entire_user.first_name,
        'id': entire_user.id,
    }
    json_user = json.dumps(user)
    return HttpResponse(json_user, status=200, content_type='application/json')

def login(req):
    post_data = json.loads(req.body.decode())
    valid, result = User.objects.login(post_data)
    if not valid:
        json_errors = json.dumps(result)
        return HttpResponse(json_errors, status=400, content_type="application/json")
    user = {
        'first_name': result.first_name,
        'id': result.id,
    }
    json_user = json.dumps(user)
    return HttpResponse(json_user, status=200, content_type="application/json")


def create_song(req):
    post_data = json.loads(req.body.decode())
    print(post_data)
    errors = Song.objects.addSongValidation(post_data)
    

    if errors:
        return HttpResponse(json.dumps(errors), status=400, content_type='application/json')

    entire_song = Song.objects.easy_create(post_data)
    song = {
        'id': entire_song.id,
        'artist': entire_song.artist,
        'title': entire_song.title,
    }
    json_song = json.dumps(song)
    return HttpResponse(json_song, status=200, content_type="application/json")

def get_songs(req):
    all_songs = Song.objects.all()
    data = serializers.serialize('json', all_songs)
    return HttpResponse(data, status=200, content_type='application/json')

def user_add_song(req):
    post_data = json.loads(req.body.decode())
    user = User.objects.get(id=post_data['user_id'])
    user.songs_added.add(Song.objects.get(id=post_data['song_id']))
    data = serializers.serialize('json', user.songs_added.all())
    return HttpResponse(data, status=200, content_type='application/json')


def songDetails(req):
    return HttpResponse("you made it to song details")