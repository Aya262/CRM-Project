from django.urls import path
from . import views

urlpatterns=[

    path('',views.home,name="home"),
    path('register/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('products/',views.products,name="products"),
    path('customers/<str:pk>/',views.customers,name="customer"),
    path('create_order/<str:pk>/',views.create_order,name="create_order"),
    path('update_order/<str:pk>/',views.update_order,name="update_order"),
    path('delete_order/<str:pk>/',views.delete_order,name="delete_order"),
    path('create_customer/',views.create_customer,name="create_customer"),
    path('customers/<str:pk>/update_customer/<str:pk2>/',views.update_customer,name="update_customer"),
    path('customers/<str:pk>/delete_customer/<str:pk2>/',views.delete_customer,name="delete_customer")


]