from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hireServiceapp.forms import UserForm, SellerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# Create your views here. i.e. functions
def home(request):
    return redirect(seller_home)

@login_required(login_url='/seller/sign-in/')
def seller_home(request):
    return render(request, 'seller/home.html', {})

def seller_sign_up(request):
    user_form = UserForm()
    seller_form = SellerForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        seller_form = SellerForm(request.POST, request.FILES)

        if user_form.is_valid() and seller_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_seller = seller_form.save(commit=False)
            new_seller.user = new_user
            new_seller.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(seller_home)

    return render(request, 'seller/sign_up.html', {
        "user_form": user_form,
        "seller_form": seller_form
    })
