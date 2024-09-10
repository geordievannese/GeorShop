from django.shortcuts import render

def home(request):
    context = {
        'app_name': 'main',
        'your_name': 'Geordie',
        'class_name': 'KKI'
    }
    return render(request, 'main.html', context)
