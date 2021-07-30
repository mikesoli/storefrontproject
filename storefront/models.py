from django.db import models
import re

from django.db.models.deletion import CASCADE
# Create your models here.

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Please enter a valid e-mail address!'
        if len(postData['email']) > 100:
            errors['email'] = 'The e-mail address you are trying to use is too long in length!'
        if len(postData['password']) < 8:
            errors ['password'] = 'Your password must be at least 8 characters in length!'
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Your passwords do not match, please try again.'
        try:
            user = User.objects.get(email = postData['email'])
            errors['email_in_use'] = 'This e-mail address is already in use by another account!'
        except:
            pass
        return errors
    
    def editvalidator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Please enter a valid e-mail address!'
        if len(postData['email']) > 100:
            errors['email'] = 'The e-mail address you are trying to use is too long in length!'
        if len(postData['password']) < 8:
            errors ['password'] = 'Your password must be at least 8 characters in length!'
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Your passwords do not match, please try again.'
        try:
            user = User.objects.get(email = postData['email'])
            errors['email_in_use'] = 'This e-mail address is already in use by another account!'
        except:
            pass
        return errors

class User(models.Model):
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Product(models.Model):
    name = models.CharField(max_length = 30)
    type = models.CharField(max_length = 30)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    image = models.CharField(max_length=1000, default='images/product0.png')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def totalcost(self):
        return self.product.price*self.quantity

