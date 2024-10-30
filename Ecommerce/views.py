from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer,user_profileSerializer,LoginSerializer,productsSerializer,CartItemSerializer,OrderItemSerializer,OrderSerializer
from .models import products,user_profile,CartItem,Order,OrderItem
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

# Create your views here.

class RegistrationView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer


class LoginView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

      
        user = authenticate(username=username, password=password)
        
        if user is not None:
            
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

class isAdmin(permissions.BasePermission):
     def has_permission(self, request, view):
          if request.method in permissions.SAFE_METHODS:
               return True
          return request.user and request.user.is_staff
    


        
class ProductListCreateApiView(generics.ListCreateAPIView):
     queryset=products.objects.all()
     serializer_class=productsSerializer
     permission_classes=[isAdmin]
     
     def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)
     
   
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
     queryset=products.objects.all()
     serializer_class=productsSerializer
     permission_classes=[isAdmin]
    
class user_profileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset=user_profile.objects.all()
    serializer_class=user_profileSerializer



class CartItemListCreateView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        product_id = self.request.data.get('product')
       
        try:
            product = products.objects.get(id=product_id)
        except products.DoesNotExist:
            raise ValidationError({"product": "Invalid product ID."})
    
        if CartItem.objects.filter(user=user, product=product_id).exists():
          return Response(
                {"error": "{product.name} is already in your cart."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        
    
        serializer.save(user=self.request.user)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):

        cart_item = self.get_object()
        quantity = request.data.get('quantity', cart_item.quantity)
        if quantity > cart_item.product.stock:
            return Response(
                {"error": f'{cart_item.product.name} of stock is not available.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # cart_item.total_price=quantity*cart_item.product.price

        cart_item.quantity = quantity
        cart_item.save()  

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)
    
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    

    def perform_create(self, serializer):
        user = self.request.user
        order_items_data = self.request.data.get('order_items')
        for item in order_items_data:
            product_id = item.get('product')
            quantity = item.get('quantity')

            # Retrieve the product from the database
            try:
                product = products.objects.get(id=product_id)
            except products.DoesNotExist:
                raise ValidationError(f"Product with ID {product_id} does not exist.")

            # Check if the requested quantity exceeds the product stock
            if quantity > product.stock:
                raise ValidationError(
                    f"Only {product.stock} stocks of {product.name} are available. "
                    f"Please order {product.stock} quantity"
                )
       
        serializer.save(user=user)  

class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
     serializer_class = OrderSerializer
     permission_classes = [permissions.IsAuthenticated]

     def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    