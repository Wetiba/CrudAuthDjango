from __future__ import unicode_literals
from django_daraja.mpesa import utils
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django_daraja.mpesa.core import MpesaClient
from decouple import config
from datetime import datetime

from django.shortcuts import render, redirect
from .models import Product
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')


@login_required
def add_product(request):
    if request.method == "POST":
        prod_name = request.POST.get("p-name")
        prod_quantity = request.POST.get("p-qtty")
        prod_size = request.POST.get("p-size")
        prod_price = request.POST.get("p-price")
        context = {
            "prod_name": prod_name,
            "prod_quantity": prod_quantity,
            "prod_size": prod_size,
            "prod_price": prod_price,
            "success": "Data saved successfully"
        }
        query = Product(name=prod_name, qtty=prod_quantity,
                        size=prod_size, price=prod_price)
        query.save()
        return render(request, 'add-product.html', context)
    return render(request, 'add-product.html')


@login_required
def products(request):
    all_products = Product.objects.all()
    context = {"all_products": all_products}
    return render(request, 'products.html', context)


@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('all-products')


@login_required
def update_product(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    if request.method == "POST":
        updated_name = request.POST.get('p-name')
        updated_qtty = request.POST.get('p-qtty')
        updated_size = request.POST.get('p-size')
        updated_price = request.POST.get('p-price')
        product.name = updated_name
        product.qtty = updated_qtty
        product.size = updated_size
        product.price = updated_price
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('all-products')
    return render(request, 'update-product.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully')
            return redirect('user-registration')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def shop(request):
    all_products = Product.objects.all()
    context = {"all_products": all_products}
    return render(request, 'shop.html', context)


mpesa_client = MpesaClient()
stk_push_callback_url = 'https://api.darajambili.com/express-payment'


def auth_success(request):
    response = mpesa_client.access_token()
    return JsonResponse(response, safe=False)


def pay(request, id):
    product = Product.objects.get(id=id)
    context = {"product": product}
    if request.method == "POST":
        amount = request.POST.get('p-price')
        amount = int(amount)
        phone_number = request.POST.get('c-phone')
        account_ref = "PAYMENT_1"
        transaction_desc = "Paying for a product"
        transaction = mpesa_client.stk_push(phone_number,amount,
                                            account_ref, transaction_desc,
                                            stk_push_callback_url)
        return JsonResponse(transaction.response_description, safe=False)
    return render(request, 'pay.html', context)

