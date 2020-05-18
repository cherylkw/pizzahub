from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.urls import reverse
from django.db.models import Sum
from django.db.models.functions import Round
from .models import Category,UserOrder,Food,FoodWithSize,UserOrder,Cart,CartItem
import stripe
import datetime

# stripe api key
stripe.api_key = settings.STRIPE_SECRET_KEY

# homepage
def index(request):
   if request.user.is_superuser:
      return redirect('admin_dashboard','Paid')
   elif request.user.is_authenticated:
      return redirect('menu',1)
   else:
      context = {
         "user":request.user,
         "Category": Category.objects.all()
      }
      return render(request,"orders/index.html",context)

# display menu items on a page
# Param : category - category id to retrieve the lists from food models
#
def menu(request,category):
   context = {
      "user" : request.user,
      "viewCat" : Category.objects.get(pk=category),
      "Category": Category.objects.all(),
      "FoodWithSize" : FoodWithSize.objects.filter(cat=category),
      "Food" : Food.objects.filter(cat=category)
   }
   return render(request,"orders/menu.html",context)

# retrieve food details in food table
# Param : cat - category to check if request is in FoodWithSize model
#         food_id - id to retrieve it's related food list in FoodWithSize model
#         size - to retrieve food price base on requested size
# Return : food name and food price
#
def searchfoodwithsize(cat,food_id,size):
   try:
      in_foodwithsize = FoodWithSize.objects.filter(cat=cat)
   except (KeyError,FoodWithSize.DoesNotExist):
      found = False 
   else:
      food_with_size = FoodWithSize.objects.get(pk=food_id)
      food_name = food_with_size.name
      if size == "S" :
         food_price = food_with_size.small_price
      else:
         food_price = food_with_size.large_price
   return food_name,food_price

# retrieve food details in food table
# Param : cat - category to retrieve it's related food list in Food model
#         food_id - id to retrieve it's related food list in Food model
# Return : food name and food price
#
def searchfood(cat,food_id):
   try:
      in_food = Food.objects.filter(cat=cat)
   except (KeyError,Food.DoesNotExist):
      found = False 
   else:
      food = Food.objects.get(pk=food_id)
      food_name = food.name
      food_price = food.price
   return food_name,food_price

# add selected items in user shopping cart
# Param : cat_id,food_id,size,type - required info in Cart model
#
@login_required()         
def addcart(request,cat_id,food_id,size,type):
   cat = Category.objects.get(pk=cat_id)
   if type == 'W':
      # search if the food order is in FoodWithSize DB
      food_name,food_price = searchfoodwithsize(cat,food_id,size)
   else:
      # search if the food order is in Food DB
      food_name,food_price = searchfood(cat,food_id)

   # retrieve all needed info and create Cart for user
   try:   
      add_item = CartItem(cat_id=cat,food_id=food_id,name=food_name,price=food_price,subtotal=food_price,size_type=size)
      add_item.save()
      find_cart = Cart.objects.get(user=request.user,status="Create")
   except (KeyError, Cart.DoesNotExist):
      add_cart = Cart(user=request.user)
      add_cart.save()
      add_cart.item.add(add_item)
      add_cart.save()
   else:
      find_cart.item.add(add_item)
   user_cart = Cart.objects.get(user=request.user,status="Create")
   return redirect('viewcart')

# retrieve cart history for customers, items are in cart which hasn't checkout yet.
@login_required()
def viewcart(request):
   try:
      cart = Cart.objects.get(user=request.user,status='Create')
   except (ValueError,KeyError,Cart.DoesNotExist):
      context = {
         "user": request.user,
         "Category": Category.objects.all(),
      }
   else:
      context = {
         "user": request.user,
         "Category": Category.objects.all(),
         "Total" : Cart.objects.get(user=request.user,status='Create').get_cart_total(),
         "Usercart" : Cart.objects.filter(user=request.user,status='Create')
      }
   return render(request,"orders/viewcart.html",context)

# update cart when customers add/update quantity/delete items in cart, not yet checkout.
@login_required()
def updatecart(request):
   cart = Cart.objects.get(user=request.user,status='Create').get_cart_items()
   for item in cart:
      itemid = item.id
      quanname = '{0}{1}'.format('quan',itemid)
      newquantity =  int(request.POST[quanname])
      if newquantity > 0 :
         newsubtotal = item.price * newquantity
         item.quantity = newquantity
         item.subtotal = newsubtotal
         item.save()
      else:
         CartItem.objects.filter(pk=itemid).delete()
   num = Cart.objects.get(user=request.user,status='Create').get_cart_items_num()
   if num == 0:
      Cart.objects.get(user=request.user,status='Create').delete()
   return redirect('viewcart')

# checkout the cart and connect stripe API by token generate from Stripe
@login_required()
def checkout(request, **kwargs):
   existing_order = Cart.objects.get(user=request.user,status='Create')
   publishKey = settings.STRIPE_PUBLISHABLE_KEY
   if request.method == 'POST':
      token = request.POST.get('stripeToken', False)
      if token:
         try:
               charge = stripe.Charge.create(
                  amount= round(existing_order.get_cart_total()*100),
                  currency='usd',
                  description='Example charge',
                  source=token,
               )

               return redirect(reverse('update_transcation_records',
                     kwargs={
                           'token': token
                     })
                  )
         except stripe.error.CardError:
               message.info(request, "Your card has been declined.")
      else:
         result = transact({
               'amount': existing_order.get_cart_total(),
               'payment_method_nonce': request.POST['payment_method_nonce'],
               'options': {
                  "submit_for_settlement": True
               }
         })

         if result.is_success or result.transaction:
               return redirect(reverse('update_transcation_records',
                     kwargs={
                           'token': result.transaction.id
                     })
                  )
         else:
               for x in result.errors.deep_errors:
                  messages.info(request, x)
               return redirect(reverse('checkout'))
         
   context = {
      "user": request.user,
      "Total" : Cart.objects.get(user=request.user,status='Create').get_cart_total(),
      "Usercart" : Cart.objects.filter(user=request.user,status='Create'),
      "STRIPE_PUBLISHABLE_KEY": publishKey
   }

   return render(request, 'orders/checkout.html', context)

# if checkout success, create user order and update status in Cart Model
@login_required()
def update_transaction_records(request, token):
   # lookup the user cart to be checkout
   checkout_order = Cart.objects.get(user=request.user,status='Create')
   total = checkout_order.get_cart_total()
   total_amt = round(total,2)
   # create user order
   userorder = UserOrder(user=request.user,total_amount=total_amt,status='Paid')
   userorder.save()

   # update the placed order
   checkout_order.status='Ordered'
   checkout_order.order_id=userorder
   checkout_order.save()
   
   messages.info(request, "Thank you! Your purchase was successful!")
   return redirect(reverse('success'))

# redirect to purchase success page once the checkout and payment transcation is completed
def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'orders/purchase_success.html', {})

# order history page for customer to view their orders
@login_required
def orderhistory(request):
   context = {
      "user" : request.user,
      "Category": Category.objects.all(),
      "UserOrder" : UserOrder.objects.filter(user=request.user),
   }
   return render(request, 'orders/order_history.html',context)

# display order items in order history and in admin page
# Param : orderid - retrieve items in user order by order id
#         type - to determine items details displayed on admin page (type = A) or customer page (type=N)
#
@login_required
def viewitems(request, orderid, type):
   if type is 'A':
      context = {
         "user" : request.user,
         "type" : 'A',
         "orderid" : orderid,
         "UserOrder" : UserOrder.objects.all(),
         "ordernumber" : UserOrder.objects.get(id=orderid).order_number,
         "orderstatus" : UserOrder.objects.get(id=orderid).status,
         "orderdate" : UserOrder.objects.get(id=orderid).user_order_date,
         "customer" : UserOrder.objects.get(id=orderid).user,
         "completedate" : UserOrder.objects.get(id=orderid).user_order_complete_date,
         "ItemList" : Cart.objects.select_related('order_id').filter(order_id__id=orderid)
      }
      return render(request,'orders/admin_dashboard.html',context)
   else :
      context = {
         "user" : request.user,
         "orderid" : orderid,
         "Category" : Category.objects.all(),
         "UserOrder" : UserOrder.objects.filter(user=request.user),
         "ordernumber" : UserOrder.objects.get(id=orderid).order_number,
         "ItemList" : Cart.objects.select_related('order_id').filter(order_id__id=orderid)
      }
      return render(request, 'orders/order_history.html',context)

# display user orders in admin dashboard
# Param : rec_status - retrieve user order by status
#         status "Paid" - user paid the order and waiting for delivery
#         status "Completed" - order already delivery
#         status "All" - display all orders
#
def admindashboard(request,rec_status):
   if rec_status == 'Paid':
      context = {
         "user" : request.user,
         "type" : 'N',
         "active1" : 'active',
         "UserOrder" : UserOrder.objects.filter(status='Paid').order_by('id'),
         "totalorder" : '('+ str(UserOrder.objects.filter(status='Paid').count()) +' Orders)'
      }
   elif rec_status == 'Completed':
      context = {
         "user" : request.user,
         "type" : 'N',
         "active2" : 'active',
         "UserOrder" : UserOrder.objects.filter(status='Completed').order_by('id'),
         "totalorder1" : '('+ str(UserOrder.objects.filter(status='Completed').count()) +' Orders)'
      }
   else:
      context = {
         "user" : request.user,
         "type" : 'N',
         "active3" : 'active',
         "UserOrder" : UserOrder.objects.all().order_by('id'),
         "totalorder2" : '('+ str(UserOrder.objects.all().count()) +' Orders)'
      }
   return render(request,'orders/admin_dashboard.html',context)

# complete the order by admin once it's delivered
# Param : orderid - update the User Order Model status to "Completed"
#
def completeorder(request,orderid):
   userorder = UserOrder.objects.get(id=orderid)
   userorder.status = 'Completed'
   userorder.complete_date = datetime.datetime.now()
   userorder.save()
   return redirect('admin_dashboard', 'Completed')
