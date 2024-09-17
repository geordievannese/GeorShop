from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from .models import Product
from .forms import ProductForm
from django.shortcuts import render, redirect

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
        'form': form
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