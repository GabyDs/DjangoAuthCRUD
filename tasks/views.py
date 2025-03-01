from django.shortcuts import render, redirect

# modulo para manejar la sesion del usuario
from django.contrib.auth import login, logout, authenticate

# modulo de formulario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# modelo de usuarios
from django.contrib.auth.models import User

# modulo de error para datos duplicados
from django.db import IntegrityError

# modulo de formulario personalizado
from .forms import TaskForm

from .models import Task


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
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, "tasks.html", {"tasks": tasks})


def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {
                    "form": TaskForm,
                    "error": "A ver mongolito, escribime bien los datos che!",
                },
            )


def signout(request):
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:

        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Escribiste mal el usuario o la contraseña bobo!",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")
