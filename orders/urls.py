from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("menu/<str:category>", views.menu, name="menu"),
    path("viewitems/<int:orderid>/<str:type>",views.viewitems,name="viewitems"),
    path("viewcart",views.viewcart,name="viewcart"),
    path("updatecart",views.updatecart,name="updatecart"),
    path("order_history",views.orderhistory,name="orderhistory"),
    path("admin_dashboard/<str:rec_status>",views.admindashboard,name="admin_dashboard"),
    path("completeorder/<int:orderid>",views.completeorder,name="completeorder"),
    path("addcart/<int:cat_id>/<int:food_id>/<str:size>/<str:type>", views.addcart, name="addcart"),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^update-transaction/(?P<token>[-\w]+)/$', views.update_transaction_records,name='update_transcation_records'),
    url(r'^purchase_success/$', views.success, name='success'),
    path("", views.index, name="index")
]
