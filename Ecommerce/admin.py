from django.contrib import admin
from .models import user_profile,products,CartItem,Order,OrderItem

# Register your models here.

@admin.register(user_profile)
class user_profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'DOB')

admin.site.register(products)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)