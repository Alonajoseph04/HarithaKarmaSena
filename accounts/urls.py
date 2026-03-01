from django.urls import path
from .views import login_page, worker_dashboard, logout_user, scan_qr, ward_summary, household_dashboard

urlpatterns = [
    path("login/", login_page, name="login"),
    path("worker/", worker_dashboard, name="worker_dashboard"),
    path("household/",household_dashboard, name="household_dashboard"),
    path("logout/", logout_user, name="logout"),  # Placeholder for logout view
    path("ward_summary/", ward_summary, name="ward_summary"),
    path("scan/", scan_qr, name="scan_qr"),
]