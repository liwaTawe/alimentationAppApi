from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *
from rest_framework.permissions import  IsAuthenticated

from accounts.models import Producer
from rest_framework import status

class DemoView(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"success": "Hi! you are authenticated"})

  


class CategoryApiView(APIView):
    
    def get(self, *args, **Kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many = True)
        return Response(serializer.data)
    
    

class ProductApiView(APIView):
    
    def get(self, request, *args, **Kwargs):
        category = self.request.query_params.get("category")
        if category:
            queryset = Product.objects.filter(category__name = category)
        else:
            queryset =  Product.objects.all()
        serializer = ProductSerialiser(queryset, many = True)
        return Response({"count": len(serializer.data), 'data': serializer.data})
    
    def post(self, request, format = None):
        user = request.user
        data =request.data

        if user.role == User.PRODUCER:
            serializer = ProductSerialiser(data = data) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_201_CREATED)  
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 
        else:
            return Response("Vous n'êtes pas autorisé à ajouter des produits", status=status.HTTP_403_FORBIDDEN)

  

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user = user, ordered = False).first()
        queryset = CartItems.objects.filter(cart = cart)
        serializer = CartItemsSerializer(queryset, many = True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        cart,_ = Cart.objects.get_or_create(user = user, ordered =False )
        product = Product.objects.get(id = data.get("product"))

        if product:
            price = product.price
            quantity = data.get("quantity")
            cart_items = CartItems(cart = cart, user = user, product = product, price = price, quantity = quantity)
            cart_items.save()

            total_price = 0
            cart_items = CartItems.objects.filter(user = user, cart = cart.id)
            for items in cart_items:
                total_price = total_price+items.price
                cart.total_price = total_price
            cart.save()
             

   
            return Response({"success": f"Items added to your cart{cart.id}"})
        else: 
            return Response({"error": "select product"})

    


    def put(self, request):
        data = request.data
        cart_item = CartItems.objects.get(id = data.get('id'))
        quantity = data.get('quantity')
        cart_item += quantity
        return Response({"success": "Items updated"})

    def delete(self, request):
        user = request.user
        data = request.data


        cart_item = CartItems.objects.get(id = data.get('id'))
        cart_item.delete()

        cart = Cart.objects.filter(user = user, ordered = False).first()
        queryset = CartItems.objects.filter(cart = cart)
        serializer = CartItemsSerializer(queryset, many = True)
        return Response(serializer.data)
    


class OrderApi(APIView): 
    
    def get(self, request):
       queryset = Orders.objects.filter(user = request.user)
       serializer = OrderSerializer(queryset, many = True)
       return Response(serializer.data)
    #data = request.data
    
    def post(self, request, format=None):
        
        user = request.user

        try:
            cart = Cart.objects.get(user=user, ordered=False)
        
        except Cart.DoesNotExist:
            return Response("Panier non trouvé ou non validé", status=status.HTTP_404_NOT_FOUND)
        
        #if cart.cart_items.count() == 0:
            #return Response("Le panier est vide, impossible de créer une commande", status=status.HTTP_400_BAD_REQUEST)
        total_price = cart.total_price
        order = Orders(user=user, cart=cart, amount=total_price)
        order.save()
        cart.ordered = True
        cart.save()

        return Response("Commande créée avec succès", status=status.HTTP_201_CREATED)
        
      


    
    def delete(self, request, format=None):
        user = request.user
        data = request.data
        if user.role == User.ADMIN:
            try:
                order = Orders.objects.get(id = data.get('id'))
                order.delete()
                return Response("Suppression effectuée correctement", status=status.HTTP_204_NO_CONTENT)
            except Orders.DoesNotExist:
                return Response("La commande n'existe pas", status= status.HTTP_403_FORBIDDEN)
            
        return Response("Vous n'êtes pas autorisé à supprimer des commandes", status=status.HTTP_403_FORBIDDEN)


    
       
        # serializer = OrderSerializer(data=request.data)
        # if cart.ordered and serializer.is_valid():
        #     serializer.save(amount = total_price)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # return Response("Impossible de créer la commande", status=status.HTTP_400_BAD_REQUEST)



        # cart = Cart.objects.get(user = user, ordered =True)
        # #cart = Cart.objects.get(id =data.get("cart"))
        # total_price = cart.total_price
        # serializer = OrderSerializer(data=request.data)
        
        # if cart.ordered == True:
        #     Orders.amount = total_price
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
            
    