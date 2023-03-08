from rest_framework import serializers

from .models import CreditCardModel


class CreditCardSerializer(serializers.Serializer):

    exp_date = serializers.ReadOnlyField(source='format_date')
    holder = serializers.CharField(max_length=128)
    number = serializers.ReadOnlyField(source='decrypt')
    cvv = serializers.CharField(max_length=3)

    class Meta:
        model = CreditCardModel
        fields = '__all__'
