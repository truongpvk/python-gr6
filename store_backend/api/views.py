from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Product

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pwd      = request.POST['password']

        user = authenticate(request, username=username, password=pwd)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.success(request, 'Sai tên đăng nhập hoặc mật khẩu!')

    return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        phone_number = request.POST['phone-number']
        email = request.POST['email']
        pwd = request.POST['password']
        re_pwd = request.POST['repeat-password']

        if pwd == re_pwd:
            try:
                user = User.objects.create_user(username=phone_number, email=email, first_name=first_name, last_name=last_name, password=pwd)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                messages.success(request, 'Lỗi không xác định!')
                return render(request, 'signup.html')
        else:
            messages.success(request, 'Mật khẩu không khớp!')
            return render(request, 'signup.html')
            

    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def product_create(request):
    if request.method == "POST":
        name = request.POST['name']
        purchase_price = float(request.POST['purchase_price'])
        selling_price = float(request.POST['selling_price'])
        quantity = int(request.POST['quantity'])
        
        item = Product(name=name, purchase_price=purchase_price, selling_price=selling_price, quantity=quantity)
        item.save()

        messages.success(request, 'Sản phẩm tạo thành công!')

        return redirect('/')

    return render(request, 'create.html')

@login_required
def product_list(request):
    items = Product.objects.all()

    total_revenue = sum(product.selling_price * product.quantity_sold for product in items)

    total_profit = total_revenue - sum(product.purchase_price * (product.quantity + product.quantity_sold) for product in items)

    return render(request, 'list.html', {
        "items": items,
        "total_revenue": total_revenue,
        "total_profit": total_profit,
    })

def product_update(request, product_id):
    item = Product.objects.get(id=product_id)

    if request.method == "POST":
        item.name            = request.POST['name']
        item.purchase_price  = float(request.POST['purchase_price'])
        item.selling_price   = float(request.POST['selling_price'])
        item.quantity        = int(request.POST['quantity'])
        item.quantity_sold   = int(request.POST['sold_quantity'])

        item.save()

        messages.success(request, 'Sản phẩm đã cập nhật thành công!')

        return redirect('/')
    
    return render(request, 'update.html', {"item":item,})

def product_delete(request, product_id):
    item = Product.objects.get(id=product_id)
    item.delete()

    messages.success(request, 'Sản phẩm đã xoá thành công!')

    return redirect('/')

def product_sell(request, product_id):
    item = Product.objects.get(id=product_id)
    
    quantity = int(request.GET.get('quantity'))

    item.quantity -= quantity
    item.quantity_sold += quantity
    item.save()

    messages.success(request, 'Sản phẩm đã bán thành công!')

    return redirect('/')
