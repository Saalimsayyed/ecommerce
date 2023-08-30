from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager

timezone.activate('Asia/Kolkata')


class User(AbstractBaseUser, PermissionsMixin):
    
    name = models.CharField(max_length=255, default="Anonymous")
    email = models.EmailField(unique=True)
    contact = models.PositiveBigIntegerField(default=100)
    
    image = models.ImageField(upload_to='users/', default=None, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    verify_token = models.CharField(max_length=255, default="")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact']

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Product(models.Model):
    
    COLLECTIONS = (
        ("Men", "Men"),
        ("Women", "Women"),
        ("Children", "Children")
    )
    
    SIZE = (
        ("Small", "Small"),
        ("Medium", "Medium"),
        ("Large", "Large")
    )
    
    image = models.ImageField(upload_to='products/')
    name = models.CharField(max_length=255, default="Product")
    description = models.TextField()
    price = models.FloatField(default=10.0)
    size = models.CharField(choices=SIZE, max_length=100)
    collection = models.CharField(choices=COLLECTIONS, max_length=100)
    
    def __str__(self):
        return self.name
    
    
class Cart(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=1.0)
    checkout = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    
class Order(models.Model):
    
    STATUS = (
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled")
    )
    
    order_id = models.CharField(max_length=10, unique=True)
    order_items = models.ManyToManyField(Cart)
    order_by = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(default="")
    state = models.CharField(max_length=200, default="")
    amount = models.FloatField(default=0.0)
    remarks = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, max_length=100, default=STATUS[0][0])
    
    def __str__(self):
        return self.order_id