from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from . import models
from Seller import models as seller_models

# Create your views here.

def customerpage(request):
    if not(request.session.get('customer_id')):
        return redirect("login")
    customer_data=models.Customer_data.objects.get(customer_id=request.session.get('customer_id'))
    data={
        'customer_data':customer_data
    }
    return render(request, "Customers/customer.html", context=data)





def handle_product_action(request, product_id):
    if not(request.session.get('customer_id')):
        return redirect('login')
    if request.method == 'POST':
        customer = models.Customer_data.objects.get(customer_id=request.session['customer_id'])
        product = get_object_or_404(seller_models.Product_data, product_id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        action = request.POST.get('action')

        if action == 'add_to_cart':
            cart_item, created = models.Cart.objects.get_or_create(customer=customer, product=product)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            return redirect('Customers:cart')  # Redirect to the cart page

        elif action == 'buy_now':
            models.Order.objects.filter(customer=customer).delete()  # Clear existing cart items
            models.Order.objects.create(customer=customer, product=product, quantity=quantity)
            return redirect('Customers:checkout')  # Redirect to the checkout page

    return redirect('home')  # Redirect to the homepage or any other appropriate page

def cart(request):
    return render(request, "Customers/cart.html")

def checkout(request):
    return render(request, "Customers/checkout.html")

def address(request):
    return render(request, "Customers/address.html")

def orderhistory(request):
    if not(request.session.get('customer_id')):
        return redirect('login')
    order_products = models.Order.objects.filter(customer_id = request.session.get('customer_id'))
    data = {
        'order_products' : order_products 
    }
    return render(request, "Customers/orderhistory.html",context=data)


def confirm_order(request):
    return render(request, "Customers/order_confirmation.html")


