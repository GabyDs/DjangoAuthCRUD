from django.http import HttpResponse

from django.shortcuts import render

# modulo de formulario
from django.contrib.auth.forms import UserCreationForm

# modelo de usuarios
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        passwd1 = request.POST['password1']
        passwd2 = request.POST['password2']
        
        if passwd1 == passwd2:
            try:
                # register user
                username = request.POST['username']

                User.objects.create_user(username=username, password=passwd1).save()

                return HttpResponse("Bien ahi logi, creaste un usuario nuevo!")
            except:
                return HttpResponse("Ya existe ese usuario boludo!")
        else:
            return HttpResponse("Las contraseñas deben ser iguales mongolito!")