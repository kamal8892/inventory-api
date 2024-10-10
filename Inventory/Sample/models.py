from django.db import models

# Create your models here.

class Euser(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(default="example@gmail.com",unique=True)
    password = models.CharField(max_length=128)


    def __str__(self):
        return self




class Category(models.Model):
    name = models.CharField(max_length=255)
    c_id = models.IntegerField()
    description = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.name 
    

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.name
    


class Product(models.Model):
    p_name = models.CharField(max_length=255)
    p_id = models.IntegerField()
    desc = models.TextField(blank=True,null=True)
    sku = models.CharField(max_length=100)
    p_price = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.p_name


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    reorder_level = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE) 

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'
    



