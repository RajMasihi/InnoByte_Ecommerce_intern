from django.contrib.auth.models import User
from .models import user_profile,products,CartItem,Order,OrderItem
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=['username','email','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
class update_userSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['first_name','last_name','email']
    
class user_profileSerializer(serializers.ModelSerializer):
    user=update_userSerializer()
    class Meta:
        model=user_profile
        fields='__all__'
       

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True, write_only=True)

class productsSerializer(serializers.ModelSerializer):
    class Meta:
        model=products
        fields='__all__'

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    quantity = serializers.IntegerField(default=1)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'user', 'added_at','total_price']
        read_only_fields = ['added_at', 'user']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields = ['id','product', 'quantity', 'total_price']  # Include only necessary fields
        read_only_fields = ['id','total_price']

        def validate(self, attrs):
          product = attrs.get('product')
          quantity = attrs.get('quantity')
          if quantity > product.stock:
            raise serializers.ValidationError("Requested quantity exceeds available stock.")
          return attrs
    

        

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'shipping_address', 'total_amount', 'status', 'order_items']
        read_only_fields = ['id','user','total_amount'] 
        
    def create(self, validated_data):
      
        order_items = validated_data.pop('order_items')

        
        order = Order.objects.create(**validated_data)
        
     
        total_amount = 0

        
        for order_item in order_items:
            product = order_item['product']

            quantity=order_item['quantity']
            item_total_price = product.price * quantity
            order_item['total_price'] = item_total_price  
            if order_item['quantity'] > product.stock:
                raise serializers.ValidationError(f"{product.name} of {quantity} stock is not available! please order quantity {product.stock} of {product.name}")
            OrderItem.objects.create(order=order, **order_item)
            total_amount += item_total_price
            product.stock -= order_item['quantity']
            product.save()

       
        order.total_amount = total_amount
        order.save()  

        return order
    def validate_status(self, value):
        request = self.context.get('request')
        order = self.instance

       
        if request.user == order.user:
            if value != 'canceled':
                raise serializers.ValidationError("You are only allowed to cancel your order.")
        
        elif request.user.is_staff: 
            allowed_statuses = ['shipped', 'paid','delivered']
            if value not in allowed_statuses:
                raise serializers.ValidationError(f"Sellers or admin can only update status to: {', '.join(allowed_statuses)}.")
        
        else:
            raise serializers.ValidationError("You are not authorized to change the order status.")

        return value

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        request = self.context.get('request')
        order = self.instance

        # If the user is the owner (buyer), they can only cancel
        if request.user == order.user:
            if value != 'canceled':
                raise serializers.ValidationError("You are only allowed to cancel your order.")
        
        # If the user is an admin (seller), they can update to allowed statuses
        elif request.user.is_staff:  # Assuming staff or admin role is for sellers
            allowed_statuses = ['process', 'shipped', 'delivered','paid']
            if value not in allowed_statuses:
                raise serializers.ValidationError(f"Sellers can only update status to: {', '.join(allowed_statuses)}.")
        
        # Unauthorized users should not be able to update the status
        else:
            raise serializers.ValidationError("You are not authorized to change the order status.")

        return value
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
    
    
   