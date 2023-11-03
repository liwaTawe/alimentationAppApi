from django.db import models
from accounts.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
#from myShop.settings import AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField()

    class Meta :
        ordering = ('name',)

    def __str__(self):
            return self.name
        
    def get_absolute_url(self):
            return f'/{self.slug}/'
    

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    price = models.FloatField(default= 0.0)
    description = models.TextField(blank=True, null= True)
    image= models.ImageField(upload_to="uploads/", blank= True, null=True)
    date_added = models.DateTimeField(auto_now_add= True)
    stock = models.IntegerField(default = 0)

    #class Meta :
        #ordering = ('categor',)

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}'
    
    def get_image(self):
         if self.image:
              return "http://127.0.0.1:8000"+ self.image.url
         return ""
    


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.username) + " "+ str(self.total_price)



class CartItems(models.Model):
    
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
   

    def __str__(self):
        return str(self.user.username) + " "+ str(self.product.name)
    

@receiver(pre_save, sender =CartItems) 
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance'] 
    price_of_product = Product.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity*float(price_of_product.price)




class Orders(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    amount = models.FloatField(default= False)
    #order_id = models.CharField(max_length=100)
   # payment_id = models.CharField(max_length=100, blank=True)
    #payment_signature = models.CharField(max_length=100, blank=True)


class OrderItems(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete= models.CASCADE)


