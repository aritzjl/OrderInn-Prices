from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

@login_required
def logout(request):
    django_logout(request)
    return redirect('comparador_pala')

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {
            "form": AuthenticationForm
        })
    else:
        email = request.POST["email"]
        password = request.POST["password1"]
        User = get_user_model()
        user = User.objects.filter(username=email).first()

        if user is not None and user.check_password(password):
            login(request, user)
            return redirect("home")
        else:
            return render(request, "signin.html", {
                "form": AuthenticationForm,
                "error": "Usuario o contraseña incorrectos."
            })
        

