from django.urls import path
from .views import show_main, product_list_json, product_detail_json, product_list_xml, product_detail_xml

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('products/json/', product_list_json, name='product_list_json'),
    path('products/json/<uuid:pk>/', product_detail_json, name='product_detail_json'),
    path('products/xml/', product_list_xml, name='product_list_xml'),
    path('products/xml/<uuid:pk>/', product_detail_xml, name='product_detail_xml'),
]
