from django.shortcuts import render, redirect, HttpResponse
from . import models

# Create your views here.

def admin(request):
    if not(request.session.get('admin_id')):
        return redirect("login")
    admin_data=models.Admin_data.objects.get(admin_id=request.session.get('admin_id'))
    data={
        'admin_data':admin_data
    }
    return render(request, "Seller/admin.html",context=data)


def product_add(request):
    if request.method == 'POST':
        product_category = request.POST['product_category']
        product_name = request.POST['product_name']
        product_description = request.POST['product_description']
        product_price = request.POST['product_price']
        
        if all([product_category,product_name,product_description,product_price]):
            try:
                new_product=models.Product_data.objects.create(   
                product_category=product_category,
                product_name=product_name,
                product_description=product_description,
                product_price=product_price)
                if request.FILES.get('product_image'):
                    product_image = request.FILES.get('product_image')
                    new_product.product_image=product_image
                    new_product.save()
                return render(request,'Seller/product.html',context={'success': 'done'})
            except:
                return HttpResponse("data not updated")     
        return redirect('success') 
    return render(request, "Seller/product.html")




