from django.http import HttpResponse

def home(reques):
    return HttpResponse ("Hello world!")