from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField( null=True)
    image = models.ImageField(null=True, blank=True)
    product_type = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    is_recomended = models.BooleanField(default=False, null=True)
    is_available = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now=True, null=True, blank=False)
    is_checked_out = models.BooleanField(default=False, null=True, blank=False)
    is_complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return f'{self.user} {self.user.id}, is_complete={self.is_complete}, {self.orderitem_set.all()}'

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.product}x{self.quantity}'

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    seat_number = models.CharField(max_length=250, null=True)
    carriage_code = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f'carriage_code: {self.carriage_code}, seat_number: {self.seat_number}'
