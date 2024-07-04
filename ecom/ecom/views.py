from django.shortcuts import render,redirect, HttpResponse,get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from django.db import IntegrityError

from Customers import models as customers_models
from Seller import models as seller_models

# Create your views here.

def home(request):
    return render(request,"home.html")


def about(request):
    return render(request, "about.html")


def carinterior(request):
    car_int_product= seller_models.Product_data.objects.filter(product_category='car_interior' )
    data={
        "interior_product":car_int_product
    }
    return render(request, "carinterior.html", context=data)


def carexterior(request):
    car_ext_product=seller_models.Product_data.objects.filter(product_category='car_exterior')
    data={
        "exterior_product":car_ext_product
    }
    return render(request, "carexterior.html", context=data)


def carcare(request):
    car_care_product=seller_models.Product_data.objects.filter(product_category='car_care')
    data={
        "care_product":car_care_product
    }
    return render(request, "carcare.html", context=data)


def carstyling(request):
    car_style_product=seller_models.Product_data.objects.filter(product_category='car_styling')
    data={
        "styling_product":car_style_product
    }
    return render(request, "carstyling.html", context=data)


def bulkdiscount(request):
    return render(request, "bulkdiscount.html")


def returnpolicy(request):
    return render(request, "returnpolicy.html" )


def contactus(request):
    return render(request, "contactus.html")


def signup(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['confirmpassword']
        gender=request.POST['gender']
        role=request.POST['role']
        phonenumber=request.POST['phone']
        if all([name,email,password,confirmpassword,gender,role,phonenumber]):
            if role=="Seller" and seller_models.Admin_data.objects.filter(admin_role__iexact='Seller').exists():
                error={'error':'seller exist'}
            elif role=='Seller':
                
                if password == confirmpassword:
                    encrypt_password= make_password(password)
                    try:
                        seller_models.Admin_data.objects.create(admin_name=name,
                                                         admin_email=email,
                                                         admin_password=encrypt_password,
                                                         admin_gender=gender,
                                                         admin_role=role,
                                                         admin_phone=phonenumber)
                        return render(request,'signup.html', context={'success':'done'})
                    except IntegrityError as e:
                        if'admin_phone'in str(e):
                            error={
                                'error':'Phone-error'
                            }
                        else:
                            error={
                                'error':'email-error'
                            }
                else:
                    error={
                        'error':'password-mismatch'
                    }
                return render(request, 'signup.html', context=error)    
            
            elif role=="Customer":
                if password == confirmpassword:
                    encrypt_password= make_password(password)
                    try:
                        customers_models.Customer_data.objects.create(customer_name=name,
                                                         customer_email=email,
                                                         customer_password=encrypt_password,
                                                         customer_gender=gender,
                                                         customer_role=role,
                                                         customer_phone=phonenumber)
                        return render(request,'signup.html', context={'success':'done'})
                    except IntegrityError as e:
                        if'customer_phone'in str(e):
                            error={
                                'error':'Phone-error'
                            }
                        else:
                            error={
                                'error':'email-error'
                            }
                else:
                    error={
                        'error':'password-mismatch'
                    }
        else:
                error={
                    'error':'empty-fields'
                }
        return render(request, 'signup.html', context=error)    
    return render(request, "signup.html")

def login(request):
    if request.POST:
        email=request.POST.get('email')
        password=request.POST.get('password')

        if customers_models.Customer_data.objects.filter(customer_email=email).exists():
            user="customer"
        elif seller_models.Admin_data.objects.filter(admin_email=email).exists():
            user="admin"


        if all([[email,password,user]]):
            if user=="customer":
                check_email = customers_models.Customer_data.objects.filter(customer_email=email).exists()
                if check_email:
                    customer = customers_models.Customer_data.objects.get(customer_email=email)
                    check_pass = check_password(password,customer.customer_password)
                    if check_pass:
                        request.session['customer_id'] = customer.customer_id
                        request.session['customer_name'] = customer.customer_name
                        request.session['customer_role'] = user
                        return redirect('Customers:customer_page')
                    
                    else:
                        error = {
                            'error' : 'not-matched'
                        }
                else:
                    error = {
                        'error': 'not-matched'
                    }
            elif user=="admin":
                check_email = seller_models.Admin_data.objects.filter(admin_email=email).exists()
                if check_email:
                    admin = seller_models.Admin_data.objects.get(admin_email=email)
                    check_pass = check_password(password,admin.admin_password)
                    if check_pass:
                        request.session['admin_id'] = admin.admin_id
                        request.session['admin_name'] = admin.admin_name
                        request.session['admin_role'] = user
                        return redirect('Seller:admin_dashboard')
                    
                    else:
                        error = {
                            'error' : 'not-matched'
                        }
                else:
                    error = {
                        'error': 'not-matched'
                    }
        else:
            error = {
                'error' : 'empty-fields'
            }
                
        return render(request, 'login.html',context=error)
    
    return render(request, "login.html")


            

def logout(request):
        if 'customer_role' in request.session:
            request.session.pop('customer_id', )
            request.session.pop('customer_name')
            request.session.pop('customer_role')
        elif 'admin_role' in request.session:
            request.session.pop('admin_id')
            request.session.pop('admin_name')
            request.session.pop('admin_role')
        return redirect('login')
    



