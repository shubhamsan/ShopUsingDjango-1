from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    name= models.CharField(max_length=50)
    shortdesc=models.TextField(max_length=100)
    desc= models.TextField(max_length=5000)
    category = models.CharField(max_length=50, default="")
    price= models.DecimalField(max_digits=10,decimal_places=0)
    image= models.ImageField(upload_to='shop/images',default="")
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    first = models.CharField(max_length=100)
    last= models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.first
    
class Orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=11)
    zip_code=models.CharField(max_length=11)
    phone = models.CharField(max_length=70, default="")


    def __str__(self):
        return self.name

