from django.urls import path
from product.views import *

urlpatterns = [  
    path("product/", ProductApiView.as_view()),
    path("category/", CategoryApiView.as_view()),
    path("orders/", OrderApi.as_view()),

    path("cart", CartView.as_view()),
    path("cartItem", Cart),
    path('demo', DemoView.as_view()),

]