from django.shortcuts import render, redirect

# modulo para manejar la sesion del usuario
from django.contrib.auth import login, logout

# modulo de formulario
from django.contrib.auth.forms import UserCreationForm

# modelo de usuarios
from django.contrib.auth.models import User

# modulo de error para datos duplicados
from django.db import IntegrityError


# Create your views here.
def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # register user
                username = request.POST["username"]

                user = User.objects.create_user(
                    username=username, password=request.POST["password1"]
                )
                user.save()

                login(request, user)

                return redirect("tasks")
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {
                        "form": UserCreationForm,
                        "error": "Ya existe ese usuario boludo!",
                    },
                )
        else:
            return render(
                request,
                "signup.html",
                {
                    "form": UserCreationForm,
                    "error": "Las contraseñas deben ser iguales mongolito!",
                },
            )


def tasks(request):
    return render(request, "tasks.html")


def signout(request):
    logout(request)
    return redirect("home")
