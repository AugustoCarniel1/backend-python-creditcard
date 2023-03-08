from datetime import datetime

from django.db import models

from .helpers import read_keys
from .utils import decrypt_credit_card_number


class CreditCardBrand(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):

        return self.description


class CreditCardModel(models.Model):
    exp_date = models.DateField()
    holder = models.CharField(max_length=128)
    number = models.TextField()
    cvv = models.IntegerField(blank=True)
    brand = models.ForeignKey(CreditCardBrand, on_delete=models.CASCADE)

    def __str__(self):
        return self.holder + "'s Credit Card"

    def decrypt(self):
        private_key = read_keys('private')

        return decrypt_credit_card_number(private_key, self.number)

    def format_date(self):

        return self.exp_date.strftime("%m/%Y")
