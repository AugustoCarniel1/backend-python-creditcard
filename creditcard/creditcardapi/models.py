import base64

from django.db import models


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
    sal = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.holder + "'s Credit Card"

    # def set_data(self, data):
    #     self.number = base64.encodestring(data)

    # def get_data(self):
    #     return base64.decodestring(self.number)

    # data = property(get_data, set_data)
