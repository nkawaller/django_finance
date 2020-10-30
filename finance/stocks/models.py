from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# https://stackoverflow.com/questions/55780537/how-to-fix-field-defines-a-relation-with-the-model-auth-user-which-has-been-s
User = settings.AUTH_USER_MODEL


# Create your models here.

class Transaction(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    stock = models.CharField('Stock', max_length=10)
    name = models.CharField('name', max_length=10)
    price = models.DecimalField('Price', max_digits=19, decimal_places=2)
    shares = models.IntegerField('Shares')
    buysell = models.CharField('Buy/Sell', max_length=10)
    datetime = models.DateTimeField('Date/Time', auto_now=False, auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.stock}, {self.shares}, {self.buysell}, {self.price}'


# Custom User Model info
# https://wsvincent.com/django-custom-user-model-tutorial/
class CustomUser(AbstractUser):
    cash = models.DecimalField('Cash', max_digits=19, decimal_places=2, default=10000)

    def __str__(self):
        return f'{self.username}'

