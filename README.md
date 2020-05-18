# Pizza Hub - Ecommerce

Web Programming with Python and JavaScript

## Welcome to Pizza Hub

Pizza Hub is a **Django project** , an ecommerce application for handling a pizza restaurant’s online orders. Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.

- **Menu**: Support all of the available menu items for Pinnochio’s Pizza & Subs (a popular pizza place in Cambridge).
- **Adding Items**: Using Django Admin, site administrators (restaurant owners) are able to add, update, and remove items on the menu. Add all of the items from the Pinnochio’s menu into database using either the Admin UI or by running Python commands in Django’s shell.
- **Registration, Login, Logout**: Site users (customers) are able to register for Pizza Hub with a username, password, first name, last name, and email address. Customers should then be able to log in and log out of the website.
- **Shopping Cart**: Once logged in, users should see a representation of the restaurant’s menu, where they can add items (along with toppings or extras, if appropriate) to their virtual “shopping cart.” The contents of the shopping should be saved even if a user closes the window, or logs out and logs back in again.
- **Placing an Order**: Once there is at least one item in a user’s shopping cart, they should be able to place an order, whereby the user is asked to confirm the items in the shopping cart, and the total before placing an order.
- **Viewing Orders**: Site administrators should have access to a page where they can view any orders that have already been placed.
- **Admin Panel**: Allowing site administrators to mark orders as complete and allowing users to see the status of their pending or completed orders.
- **Checkout Method**: Integrating with the **Stripe API** to allow users to actually use a credit card to make a purchase during checkout.

## Functions functionality in views.py

- index(request) : homepage
- menu(request,category) : display menu
- searchfoodwithsize(cat,food_id,size) : retrieve food details in food table
- searchfood(cat,food_id) : retrieve food details in food table
- addcart(request,cat_id,food_id,size,type) : add selected items in user shopping cart
- viewcart(request) : retrieve cart history for customers, items are in cart which hasn't checkout yet
- updatecart(request) : update cart when customers add/update quantity/delete items in cart, not yet checkout
- checkout(request, **kwargs) : checkout the cart and connect stripe API by token generate from Stripe
- update_transaction_records(request, token) : if checkout success, create user order and update status in Cart Model
- success(request, **kwargs) : redirect to purchase success page once the checkout and payment transcation is completed
- orderhistory(request) : order history page for customer to view their orders
- viewitems(request, orderid, type) : display order items in order history and in admin page
- admindashboard(request,rec_status) : display user orders in admin dashboard
- completeorder(request,orderid) : complete the order by admin once it's delivered

## HTML

- index.html : homepage
- admin_dashboard : admin page for handling user orders
- checkout.html : a page for checking out the order by customer
- menu.html : display items in the food menu
- messages.html : a template for displaying any site messages
- checkout_layout.html : a template page for checkout page
- layout.html : a template for whole site
- order_history.html : display the order records for customers
- purchase_success.html : Stripe redirects to this page after purchase successed
- viewcart.html : a page to display items in the cart

## ECMAScript

- checkout.js : functions for Stripe Checkout
- order.js : add or remove items in cart page by triggering the plus and minus sign

## CSS

- checkout.css : styling for checkout page only
- styles.css : styling for the whole site

## Youtube Demo

https://youtu.be/rem3EXd1p3c

## Pre-requisites and programs used versions

-  Python 3.6 or higher
-  the latest version of pip

## Setting up the development environment

1. git clone this project

2. Run **pip3 install -r requirements.txt** in your terminal window to make sure that all of the necessary Python packages are installed.

3. Run **python3 manage.py makemigrations** to make sure the models are uptodate for using

4. Run **python3 manage.py migrate** for migration

5. Run **python3 manage.py runserver** to start up this Django application.

## Visiting an URL and interact with the application

- Open the localhost http://127.0.0.1:8000/ to run the app
- Signup a customer account to place order , checkout and view your order records
- Shopping cart will be kept for your next sign in
- To delete items on cart, simply click or enter 0 and update cart, the item will be deleted
- The status and details of your order will be shown on **order history** page

## Admin Function

- To visit the **Django Admin**, login to http://127.0.0.1:8000/admin
- Username1 : admin Password : admin1
- To visit site admin for order management, login to http://127.0.0.1:8000/

## Setup and Testing for Stripe checkout

**Develpoer Setup**

1. Make sure you open an account in **Stripe** 

2. After login to your **Strip** account, find **API Keys** under **Developer** column, choose **view test data** mode, copy the tokens of **Publishable key** and **Secret key**. Remember to use **test keys** , not the **live keys**.

3. Replace the keys in setting.py

**Customer testing**
- Use testing card number **4242 4242 4242 4242** to perform the testing

## Author : Cheryl Kwong  Email : cherylkwong@gmail.com
## Project developed by : Python, Django, Javascript, CSS, HTML, SQLite3, Stripe
