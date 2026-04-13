from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import GateUserCreationForm


def landing(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "web_ui_app/landing.html")


@login_required
def dashboard(request):
    return render(request, "web_ui_app/dashboard.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = GateUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = GateUserCreationForm()
    return render(request, "web_ui_app/register.html", {"form": form})
