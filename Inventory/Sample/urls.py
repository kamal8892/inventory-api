from django.urls import path
from .views import signup,Login,UserUpdate,category_api,product_api,supplier_api,inventory_api

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('login/',Login,name='login'),
    path('userupdate/',UserUpdate,name='userupdate'),
    path('category/',category_api,name='category'),
    path('category/<int:pk>/',category_api,name='category'),
    path('supplier/',supplier_api,name='supplier'),
    path('supplier/<int:pk>/',supplier_api,name='supplier'),
    path('product/',product_api,name='product'),
    path('product/<int:pk>/',product_api,name='product'),
    path('inventory/',inventory_api,name='inventory'),
    path('inventory/<int:pk>/',inventory_api,name='inventory'),
]
