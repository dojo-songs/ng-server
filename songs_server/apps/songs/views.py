from django.shortcuts import render, HttpResponse

def index(request):

    return HttpResponse("hey you made it")