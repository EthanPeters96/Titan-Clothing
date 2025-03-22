from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>',
         views.order_history, name='order_history'),
    path('product_management/',
         views.product_management, name='product_management'),
    path('add_superuser/',
         views.add_superuser, name='add_superuser'),
    path('edit_superuser/<int:user_id>/',
         views.edit_superuser, name='edit_superuser'),
    path('delete_superuser/<int:user_id>/',
         views.delete_superuser, name='delete_superuser'),
    path('add_category/',
         views.add_category, name='add_category'),
    path('edit_category/<int:category_id>/',
         views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>/',
         views.delete_category, name='delete_category'),
    path('add_product/',
         views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/',
         views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/',
         views.delete_product, name='delete_product'),
]
