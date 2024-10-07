from django.urls import path
from .views import show_main, product_list_json, product_detail_json, product_list_xml, product_detail_xml
from main.views import register
from main.views import login_user
from main.views import logout_user
from main.views import edit_product
from .views import delete_product
from main.views import add_product_entry_ajax

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('products/json/', product_list_json, name='product_list_json'),
    path('products/json/<uuid:pk>/', product_detail_json, name='product_detail_json'),
    path('products/xml/', product_list_xml, name='product_list_xml'),
    path('products/xml/<uuid:pk>/', product_detail_xml, name='product_detail_xml'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit-product/<uuid:id>', edit_product, name='edit_product'),
    path('delete/<uuid:id>/', delete_product, name='delete_product'),
    path('create-product-entry-ajax', add_product_entry_ajax, name='add_product_entry_ajax'),
]
