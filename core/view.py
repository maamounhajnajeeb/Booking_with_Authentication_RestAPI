from django.shortcuts import render
from django.conf import settings

import stripe


stripe.api_key = settings.STRIPE_PRIVATE_KEY

def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})


def logout(request):
    return render(request, "logout.html", {})

def booking(request):
    return render(request, "booking.html", {})

def index(request):
    return render(request, "landing_page.html", {})

def charge_view(request):
    if request.method == "POST":
        amount = int(request.POST["amount"])
        customer = stripe.Customer.create(
            email=request.user.email,
            name=request.user.username,
            source=request.POST['stripeToken'],
        )
        stripe.Charge.create(
            customer=customer, amount=amount*100,
            currency="usd", description="Flight money"
        )
    return render(request, "success.html", {})
