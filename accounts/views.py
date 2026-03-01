from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect ONLY workers
            if user.groups.filter(name="Worker").exists():
                return redirect("worker_dashboard")
            else:
                messages.error(request, "User is not assigned as Worker")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")

@login_required
def worker_dashboard(request):
    if not request.user.groups.filter(name="Worker").exists():
        return HttpResponseForbidden("Access denied")

    if request.method == "POST":
        selected_ward = request.POST.get("ward")
        request.session["ward"] = selected_ward
        return redirect("ward_summary")  # 🔑 AUTO REDIRECT

    return render(request, "accounts/worker_dashboard.html")

@login_required
def ward_summary(request):
    ward = request.session.get("ward")

    house_data = {
        "Ward 1": 120,
        "Ward 2": 95,
        "Ward 3": 140,
    }

    total_houses = house_data.get(ward, 0)
    total_amount = total_houses * 50

    return render(
        request,
        "accounts/ward_summary.html",
        {
            "ward": ward,
            "total_houses": total_houses,
            "total_amount": total_amount,
        },
    )


@login_required
def scan_qr(request):
    return render(request, "accounts/scan.html")


def logout_user(request):
    logout(request)
    return redirect('login')

