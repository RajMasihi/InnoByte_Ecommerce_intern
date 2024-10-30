from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class user_profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField(max_length=60, null=True,blank=True)
    DOB=models.DateField(null=True,blank=True)
    user_picture=models.ImageField(upload_to="users_picture/", null=True,blank=True)
    
    def __str__(self):
        return self.user.username
    
class products(models.Model):
    name=models.CharField(max_length=50, unique=True)
    product_picture=models.ImageField(max_length=50,upload_to="products_picture" ,default='null.jpg', blank=True,null=True)
    description=models.TextField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.IntegerField()
    added_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class CartItem(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'pending'),
        ('paid', 'paid'),
        ('shipped', 'shipped'),
        ('delivered', 'delivered'),
        ('canceled', 'canceled'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    shipping_address=models.TextField()
    total_amount=models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=STATUS_CHOICES,default='pending', max_length=25)
    updated_at=models.DateTimeField(auto_now=True)

   

    def __str__(self):
        return f"Order id {self.id} by {self.user.username} total amount {self.total_amount}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
   

    def __str__(self):
        return f"{self.order.user.username} buy {self.quantity} items of {self.product.name} total price {self.total_price} "


    


