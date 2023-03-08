from rest_framework import serializers

from .helpers import read_keys
from .models import CreditCardModel
from .utils import decrypt_credit_card_number

private_key = read_keys('private')


class CreditCardSerializer(serializers.Serializer):

    exp_date = serializers.DateField()
    holder = serializers.CharField(max_length=128)
    number = serializers.ReadOnlyField(source='decrypt')
    cvv = serializers.CharField(max_length=3)

    class Meta:
        model = CreditCardModel
        fields = '__all__'
