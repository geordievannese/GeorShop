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

@login_required(login_url='/login')
def show_main(request):
    form = ProductForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('main:show_main')  # Redirect to prevent resubmission

    product_entries = Product.objects.all()

    context = {
        'name': 'Geordie',
        'class': 'PBP KKI',
        'npm': '2306170414',
        'product_entries': product_entries,
        'form': form,
        'last_login': request.COOKIES['last_login'],
    }
    
    return render(request, "main.html", context)

def product_list_json(request):
    products = Product.objects.all()
    data = list(products.values('id', 'name', 'price', 'description'))
    return JsonResponse(data, safe=False)

def product_detail_json(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse({
        'name': product.name,
        'price': product.price,
        'description': product.description
    })

def product_list_xml(request):
    products = Product.objects.all()
    data = serialize('xml', products)
    return HttpResponse(data, content_type='application/xml')

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
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return redirect('main:show_main')

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return redirect('main:login')