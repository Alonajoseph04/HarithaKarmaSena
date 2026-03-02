
from waste.models import Collection
from waste.models import Ward
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.utils.timezone import now

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Role-based redirection
            if user.is_superuser:
                return redirect("/admin/")

            elif user.groups.filter(name="Worker").exists():
                return redirect("worker_dashboard")

            elif user.groups.filter(name="Household").exists():
                return redirect("household_dashboard")

            else:
                messages.error(request, "User role not assigned.")
                return redirect("login")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")
@login_required
def worker_dashboard(request):
    if not request.user.groups.filter(name="Worker").exists():
        return HttpResponseForbidden("Access denied")

    # If ward selected from dropdown
    if request.method == "POST" and request.POST.get("ward"):
        request.session["ward"] = request.POST.get("ward")
        return redirect("worker_dashboard")

    # If change ward button pressed
    if request.method == "POST" and request.POST.get("ward") == "":
        request.session.pop("ward", None)
        return redirect("worker_dashboard")

    selected_ward = request.session.get("ward")

    if selected_ward:
        try:
            ward_obj = Ward.objects.get(name=selected_ward)
        except Ward.DoesNotExist:
            request.session.pop("ward", None)
            return redirect("worker_dashboard")

        total_houses = ward_obj.total_houses
        total_amount = ward_obj.total_amount

        collected_count = Collection.objects.filter(
            worker=request.user,
            ward=selected_ward,
            date=now().date()
        ).count()

        remaining_houses = total_houses - collected_count

        per_house_amount = total_amount / total_houses if total_houses > 0 else 0
        collected_amount = round(collected_count * per_house_amount, 2)
        remaining_amount = round(total_amount - collected_amount, 2)

        progress_percent = (collected_count / total_houses) * 100 if total_houses > 0 else 0

        return render(request, "accounts/worker_dashboard.html", {
            "selected_ward": selected_ward,
            "total_houses": total_houses,
            "remaining_houses": remaining_houses,
            "collected_count": collected_count,
            "total_amount": total_amount,
            "collected_amount": collected_amount,
            "remaining_amount": remaining_amount,
            "progress_percent": progress_percent,
        })

    return render(request, "accounts/worker_dashboard.html")
    
@login_required
def household_dashboard(request):
    if not request.user.groups.filter(name="Household").exists():
        return HttpResponseForbidden("Access denied")

    return render(request, "accounts/household_dashboard.html")


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
    if not request.user.groups.filter(name="Worker").exists():
        return HttpResponseForbidden("Access denied")

    selected_ward = request.session.get("ward")

    if not selected_ward:
        return redirect("worker_dashboard")

    message = None

    if request.method == "POST":
        house_code = request.POST.get("house_code")

        exists = Collection.objects.filter(
            worker=request.user,
            ward=selected_ward,
            house_code=house_code,
            date=now().date()
        ).exists()

        if exists:
            message = "Already scanned today"
        else:
            Collection.objects.create(
                worker=request.user,
                ward=selected_ward,
                house_code=house_code
            )
            message = "Collection recorded"

    count = Collection.objects.filter(
        worker=request.user,
        ward=selected_ward,
        date=now().date()
    ).count()

    return render(request, "accounts/scan.html", {
        "message": message,
        "count": count
    })

def logout_user(request):
    logout(request)
    return redirect('login')

