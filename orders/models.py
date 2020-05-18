from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# auto generate the order number, inital order number is 1000
def OrderNumber():
    user_order = UserOrder.objects.all().order_by('id').last()
    if not user_order:
        order_num = 1000
    else:
        order_num = user_order.order_number + 1
    return order_num

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id} : {self.name}"

# food which has 2 sizes with different prices
class FoodWithSize(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="foodwithsize_category")
    name = models.CharField(max_length=64)
    small_price = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    large_price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.id} - {self.cat} : {self.name} / Small : ${self.small_price} / Large : ${self.large_price}"

# food which has only 1 size with or without prices
class Food(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="food_category")
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self):
        return f"{self.id} - {self.cat} : {self.name} / Price : ${self.price}"

# User order record
class UserOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_number = models.IntegerField(default=OrderNumber)
    status = models.CharField(max_length=64,default="Paid")
    total_amount = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    complete_date = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.user} - {self.order_number} - {self.status} time : {self.timestamp}"
    
    def user_order_history(self):
        return f"Order Number : {self.order_number} - Order Date : {self.timestamp.strftime('%m/%d/%Y')}"
    
    def user_order_date(self):
        return f"Order Date : {self.timestamp.strftime('%m/%d/%Y')}"

    def user_order_complete_date(self):
        return f"Complete Date : {self.complete_date.strftime('%m/%d/%Y')}"

    def user_order_number(self):     
        return f"Order Number : {self.order_number}"

# contain items in carts
class CartItem(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="cartitem_cat")
    food_id = models.IntegerField()
    name = models.CharField(max_length=64,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=4,decimal_places=2,null=True,blank=True)
    subtotal = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    size_type = models.CharField(max_length=1,default="N")
    
# cart links with cart items and user order    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_id = models.ForeignKey(UserOrder, on_delete=models.CASCADE,null=True,blank=True,related_name="userorder_id")
    item = models.ManyToManyField(CartItem,related_name="cart_item")
    status = models.CharField(max_length=64,default="Create")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_cart_items_num(self):
        return self.item.count()

    def get_cart_items(self):
        return self.item.all()

    def get_cart_total(self):
        return sum([get_item.price*get_item.quantity for get_item in self.item.all()])

    def __str__(self):
        return f"{self.user} - status : {self.status}, item: {self.item} , create time : {self.timestamp}"



