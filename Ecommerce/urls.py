from django.contrib import admin
from django.urls import path,include
from .views import RegistrationView,LoginView,ProductListCreateApiView,ProductRetrieveUpdateDestroyView,user_profileRetrieveUpdateView,CartItemListCreateView,CartItemDetailView,OrderListCreateView,OrderRetrieveUpdateView

urlpatterns = [
   path('Register/',RegistrationView.as_view(), name="register"),
   path('Login/',LoginView.as_view(), name="Login"),
   path('products/',ProductListCreateApiView.as_view(), name="create_show_products"),
   path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name="ret_update_del_products"),
   path('users/<int:pk>/',user_profileRetrieveUpdateView.as_view(),name="user_profile"),
   path('cartitems/', CartItemListCreateView.as_view(), name='cart-item-list-create'),
   path('cartitems/<int:pk>/', CartItemDetailView.as_view(), name='cart-item-detail'),
   path('orders/',OrderListCreateView.as_view(), name='orders_list_create'),
   path('orders/<int:pk>/',OrderRetrieveUpdateView.as_view(), name='orders_Retrieve_update'),

]

