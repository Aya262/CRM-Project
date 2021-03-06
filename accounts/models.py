from django.db import models

# Create your models here.

class Customer(models.Model):
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    Category=(
        ('Indoor','Indoor'),
        ('Out Door','Out Door')
    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(choices=Category,max_length=200,null=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name



class Order(models.Model):
    Status=(
        ('Pending','Pending'),
        ('Out for Delivery','Out For Delivery'),
        ('Delivered','Delivered')
    )
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product=models.ForeignKey(Products,null=True,on_delete=models.SET_NULL)
    date_created=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,null=True,choices=Status)
    note=models.CharField(max_length=1000,null=True)

    def __str__(self):
        return self.product.name
