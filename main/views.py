import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from .models import Product
from .forms import ProductForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.utils.html import escape


@login_required(login_url='/login')
def show_main(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST" :
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main') 

    product_entries = Product.objects.filter(user=request.user)
   
    context = {
        'name': request.user.username,
        'product_entries': product_entries,
        'name': 'Geordie',
        'class': 'PBP KKI',
        'npm': '2306170414',
        'form': form,
        'last_login': request.COOKIES.get('last_login', 'No last login found'),
    }

    return render(request, "main.html", context)

@login_required
def product_list_json(request):
    data = list(Product.objects.filter(user=request.user).values())
    return JsonResponse(data, safe=False)

def product_detail_json(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse({
        'name': product.name,
        'price': product.price,
        'description': product.description
    })

def product_list_xml(request):
    products = Product.objects.filter(user=request.user)
    xml_data = serialize('xml', products)
    return HttpResponse(xml_data, content_type='application/xml')

def product_detail_xml(request, pk):
    product = Product.objects.filter(pk=pk)
    xml_data = serialize('xml', product)
    return HttpResponse(xml_data, content_type='application/xml')

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                response = HttpResponseRedirect(reverse("main:show_main"))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            else:
               
                messages.error(request, "Invalid username or password. Please try again.")
        else:
           
            messages.error(request, "Invalid username or password. Please try again.")
    
  
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return redirect('main:login')

def edit_product(request, id):
 
    product = Product.objects.get(pk = id)

    # Set mood entry as an instance of the form
    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        # Save form and return to home page
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_product.html", context)

@csrf_exempt
@login_required
def delete_product(request, id):
    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=id, user=request.user)
            product.delete()
            return JsonResponse({'success': True, 'message': 'Product deleted successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = strip_tags(request.POST.get("name")) 
    description = strip_tags(request.POST.get("description")) 
    name = request.POST.get("name")
    price = request.POST.get("price")
    description = request.POST.get("description")
    user = request.user

    if not name or not price:
        return JsonResponse({"message": "Name and price are required fields."}, status=400)
    
    try:
        price = float(price)
    except ValueError:
        return JsonResponse({"message": "Price must be a number."}, status=400)

    new_product = Product(
        name=name,
        price=price,
        description=description,
        user=user
    )
    new_product.save()

    return JsonResponse({
        "message": "Product created successfully",
        "product_id": new_product.id,
        "name": new_product.name,
        "price": new_product.price,
        "description": new_product.description
    }, status=201)

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        
        new_product = Product.objects.create(
            user=request.user,  
            name=data["name"],
            price=int(data["price"]),
            description=data["description"]
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
