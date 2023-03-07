from rest_framework import serializers


class CreditCardSerializer(serializers.Serializer):

    exp_date = serializers.DateField()
    holder = serializers.CharField(max_length=128)
    number = serializers.CharField(max_length=1024)
    cvv = serializers.CharField(max_length=3)
