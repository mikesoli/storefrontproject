from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    # See models.py's registration validator for error logic.
    errors = User.objects.validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    new_user = User.objects.create(
        email=request.POST['email'],
        password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    )
    request.session['email'] = new_user.email
    request.session['id'] = new_user.id
    return redirect('/')

def login(request):
    if request.method == 'GET':
        return redirect('/')
    try: user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, 'You have entered an invalid E-mail and/or Password')
        return redirect('/')
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, 'You have entered an invalid E-mail and/or Password')
        return redirect('/')
    else:
        request.session['user_id'] = user.id
        request.session['email'] = user.email
        return redirect('/home')

def home(request):
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
    }
    return render(request, 'home.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def search(request):
    query = request.GET['search']
    products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
        'products':products,
        'query':query,
    }    
    return render(request, 'search.html', context)

def edit(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'edit.html', context)

def update(request):
    errors = User.objects.editvalidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit')
    else:
        edit_user = User.objects.get(id=request.session['user_id'])
        edit_user.email = request.POST['email']
        edit_user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        edit_user.save()
        return redirect('/home')

def categories(request):
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
    }    
    return render(request, 'categories.html', context)

def inventory(request):
    return render (request, 'inventory.html')

def addproduct(request):
    Product.objects.create(
        name=request.POST['name'],
        type=request.POST['type'],
        description=request.POST['description'],
        price=request.POST['price'],
        image=request.POST['img'],
    )
    return redirect('/inventory')

def TCG(request):
    products = Product.objects.filter(type="TCG")
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
        'products':products
    }    
    return render(request, 'TCG.html', context)

def boardgames(request):
    products = Product.objects.filter(type="Board Game")
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
        'products':products
    }    
    return render(request, 'boardgames.html', context)

def product(request, product_id):
    user_id = request.session['user_id']
    context = {
        'user': User.objects.get(id=user_id),
        'product': Product.objects.get(id = product_id),
    }
    return render(request, 'product.html', context)

def cart(request):
    user = User.objects.get(id=request.session['user_id'])
    cartproducts = CartProduct.objects.filter(user=user)
    context = {
        'user': user,
        'cartproducts': cartproducts,
        'totalcost': sum([cartproduct.totalcost for cartproduct in cartproducts])
    }
    return render(request, 'cart.html', context)

def addtocart(request, product_id):
    product = Product.objects.get(id=product_id)
    user = User.objects.get(id=request.session['user_id'])
    CartProduct.objects.create(
        product = product,
        user = user,
        quantity = request.POST['quantity'],
    )
    return redirect('/cart')

def checkout(request):
    user = User.objects.get(id=request.session['user_id'])
    cartproducts = CartProduct.objects.filter(user=user)
    context = {
        'user': user,
        'cartproducts': cartproducts,
        'totalcost': sum([cartproduct.totalcost for cartproduct in cartproducts])
    }
    cartproducts.delete()
    return render(request, 'checkout.html', context)