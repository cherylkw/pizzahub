# create tables in DB

from django.contrib import admin

from .models import Category,FoodWithSize,Food,UserOrder,CartItem,Cart

admin.site.register(Category)
admin.site.register(FoodWithSize)
admin.site.register(Food)
admin.site.register(UserOrder)
admin.site.register(Cart)
admin.site.register(CartItem)
