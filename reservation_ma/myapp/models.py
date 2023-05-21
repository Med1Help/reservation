from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name     = models.CharField(max_length=200,null=True)
    email    = models.EmailField(unique=True) 
    num      = models.CharField(max_length=10,null=True)
    role     = models.CharField(max_length=100,null=True)
    password = models.CharField(max_length=200)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Event(models.Model):
    title     = models.CharField(max_length=200,null=True)
    owner     = models.ForeignKey(User,on_delete=models.CASCADE)
    date      = models.DateField()
    time      = models.DateTimeField()
    place     = models.CharField(max_length=200)
    magniture = models.ImageField(null=True,default="avatar.svg")

class TicketRef(models.Model):
    event       = models.ForeignKey(Event,on_delete=models.CASCADE)
    price       = models.DecimalField(decimal_places=5,max_digits=5)
    ticketType  = models.CharField(max_length=200)
    ticketDispo = models.BigIntegerField()

class Client(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.CharField(max_length=200)
    cardNumber = models.BigIntegerField()
    cvv        = models.IntegerField()
    exp        = models.CharField(max_length=5)

class Ticket(models.Model):
    event       = models.ForeignKey(Event,on_delete=models.CASCADE)
    owner       = models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    price       = models.DecimalField(decimal_places=5,max_digits=5)
    ticketType  = models.CharField(max_length=200)
    date        = models.DateField()
    time        = models.DateTimeField()
    ref         = models.CharField(max_length=200)    

class Order(models.Model):
    client = models.ForeignKey(Client,on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)