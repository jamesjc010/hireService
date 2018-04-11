from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from hireServiceapp.forms import UserForm, SellerForm, UserFormForEdit, ItemForm
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from hireServiceapp.models import Item, Order


# Create your views here. i.e. functions
def home(request):
    return redirect(seller_home)

@login_required(login_url='/seller/sign-in/')
def seller_home(request):
    return redirect(seller_order)

@login_required(login_url='/seller/sign-in/')
def seller_account(request):
    user_form = UserFormForEdit(instance = request.user)
    seller_form = SellerForm(instance = request.user.seller)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        seller_form = SellerForm(request.POST, request.FILES, instance = request.user.seller)

        if user_form.is_valid() and seller_form.is_valid():
            user_form.save()
            seller_form.save()

    if request.user.seller.image:
        seller_form.fields['image'].required = False

    return render(request, 'seller/account.html', {
        "user_form": user_form,
        "seller_form": seller_form,
    })

@login_required(login_url='/seller/sign-in/')
def seller_item(request):
    #This line gets the items of seller
    items = Item.objects.filter(seller = request.user.seller).order_by("-id")
    return render(request, 'seller/item.html', {"items": items})

@login_required(login_url='/seller/sign-in/')
def seller_add_item(request):
    form = ItemForm()

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user.seller
            item.save()
            return redirect(seller_item)

    return render(request, 'seller/add_item.html', {
        "form": form,
    })

@login_required(login_url='/seller/sign-in/')
def seller_edit_item(request, item_id):
    form = ItemForm(instance = Item.objects.get(id = item_id))

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance = Item.objects.get(id = item_id))

        if form.is_valid():
            form.save()
            return redirect(seller_item)

    return render(request, 'seller/edit_item.html', {
        "form": form,
    })

@login_required(login_url='/seller/sign-in/')
def seller_order(request):
    #check if the current order has been prepared, if not have a ready button
    if request.method == "POST":
        order = Order.objects.get(id = request.POST["id"], seller = request.user.seller)

        if order.status == Order.PREPARING:
            order.status = Order.READY
            order.save()

    #if seller is current user get all orders of theirs
    orders = Order.objects.filter(seller = request.user.seller).order_by("-id")
    return render(request, 'seller/order.html', {"orders": orders})

@login_required(login_url='/seller/sign-in/')
def seller_report(request):
    return render(request, 'seller/report.html', {})

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
