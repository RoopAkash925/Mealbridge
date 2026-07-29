from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Home, Donor, Donation



def home_page(request):
    return render(request, "home.html")



def home_register(request):

    if request.method == "POST":

        organization_name = request.POST.get("organization_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        home_type = request.POST.get("home_type")
        contact_number = request.POST.get("contact_number")
        address = request.POST.get("address")
        residents = request.POST.get("residents")

        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        
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



@login_required
def home_dashboard(request):

   
    try:
        home = Home.objects.get(user=request.user)
    except Home.DoesNotExist:
        return redirect("home_register")


    donations = Donation.objects.all().order_by('-created_at')

    return render(request, "home-dashboard.html", {
        "home": home,
        "donations": donations
    })


from django.contrib.auth.models import User
from django.contrib import messages

def donor_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("donar_register")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        Donor.objects.create(
            user=user,
            name=name,
            phone=phone,
            email=email
        )

        messages.success(request, "Donor registered successfully!")
        return redirect("donar_login")

    return render(request, "donar-register.html")

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



@login_required
def donar_dashboard(request):
    return render(request, "donar-dashboard.html")



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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Donor

from django.http import HttpResponse

@login_required
def donar_profile(request):
    donor = Donor.objects.get(user=request.user)
    return HttpResponse(f"Profile loaded successfully: {donor.name}")
@login_required
def update_profile(request):
    donor = Donor.objects.get(user=request.user)

    if request.method == "POST":
        donor.name = request.POST.get("name")
        donor.phone = request.POST.get("phone")
        donor.email = request.POST.get("email")
        donor.save()

        return redirect("donar_profile")

    return render(request, "profile.html", {"donor": donor})