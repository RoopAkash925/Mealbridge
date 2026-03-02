from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Home, Donor, Donation


# ================= HOME PAGE =================
def home_page(request):
    return render(request, "home.html")


# ================= HOME REGISTER =================
def home_register(request):

    if request.method == "POST":

        organization_name = request.POST.get("organization_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        home_type = request.POST.get("home_type")
        contact_number = request.POST.get("contact_number")
        address = request.POST.get("address")
        residents = request.POST.get("residents")

        # Create Django user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Create Home profile
        Home.objects.create(
            user=user,
            organization_name=organization_name,
            home_type=home_type,
            contact_number=contact_number,
            address=address,
            residents=residents,
            email=email
        )

        messages.success(request, "Registration successful! Please login.")
        return redirect("home_login")

    return render(request, "home-register.html")


# ================= HOME LOGIN =================
def home_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home_dashboard")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "home-login.html")


# ================= HOME DASHBOARD =================
@login_required
def home_dashboard(request):

    # Ensure logged user has Home profile
    try:
        home = Home.objects.get(user=request.user)
    except Home.DoesNotExist:
        return redirect("home_register")

    # Fetch all donor donations
    donations = Donation.objects.all().order_by('-created_at')

    return render(request, "home-dashboard.html", {
        "home": home,
        "donations": donations
    })


# ================= DONOR REGISTER =================
def donor_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Create login user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Create donor profile
        Donor.objects.create(
            user=user,
            name=name,
            phone=phone
        )

        messages.success(request, "Donor registered successfully!")
        return redirect("donar_login")

    return render(request, "donar-register.html")


# ================= DONOR LOGIN =================
def donor_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("donar_dashboard")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "donar-login.html")


# ================= DONOR DASHBOARD =================
@login_required
def donar_dashboard(request):
    return render(request, "donar-dashboard.html")


# ================= CREATE DONATION =================
@login_required
def create_donation(request):

    if request.method == "POST":

        Donation.objects.create(
            donor=request.user,
            event_name=request.POST.get("event_name"),
            food_type=request.POST.get("food_type"),
            quantity=request.POST.get("quantity"),
            cooked_time=request.POST.get("cooked_time"),
            pickup_deadline=request.POST.get("pickup_deadline"),
            location=request.POST.get("location"),
            packaging=request.POST.get("packaging"),
            image=request.FILES.get("image"),
        )

        messages.success(request, "Donation added successfully!")
        return redirect("donar_dashboard")

    return redirect("donar_dashboard")