from django.db import models


class CreditCardBrand(models.Model):
    description = models.CharField(max_length=64)

    def __str__(self):

        return self.description


class CreditCardModel(models.Model):
    exp_date = models.DateField()
    holder = models.CharField(max_length=128)
    number = models.CharField(max_length=20)
    cvv = models.IntegerField(blank=True)
    brand = models.ForeignKey(CreditCardBrand, on_delete=models.CASCADE)

    def __str__(self):

        return self.holder + "'s Credit Card"
