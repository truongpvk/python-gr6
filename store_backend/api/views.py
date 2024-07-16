from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Product

# Create your views here.
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
