from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('search', views.search),
    path('cart', views.cart),
    path('home', views.home),
    path('edit', views.edit),
    path('update', views.update),
    path('categories', views.categories),
    path('logout', views.logout),
    path('inventory', views.inventory),
    path('addproduct', views.addproduct),
    path('TCG', views.TCG),
    path('boardgames', views.boardgames),
    path('product/<int:product_id>', views.product),
    path('cart/<int:product_id>', views.addtocart),
    path('checkout', views.checkout),
]