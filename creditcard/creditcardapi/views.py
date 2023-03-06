from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from creditcard import CreditCard

from .models import CreditCardModel
from .serializer import CreditCardSerializer


@api_view(["GET", "POST"])
def credit_card(request):

    if request.method == "GET":

        try:

            card_list = CreditCardModel.objects.all()

            serializer = CreditCardSerializer(card_list, many=True)

            print(serializer.data)

            return Response({
                "credit_card_list": serializer.data
            })

        except:

            return Response({
                "message": "Error 5XX"
            })

    else:

        try:

            params = request.data

            cc = CreditCard

            credit_card = CreditCardModel(
                exp_date=params["exp_date"],
                holder=params["holder"],
                number=params["number"],
                cvv=params["cvv"]
            )

            credit_card.save()

            serializer = CreditCardSerializer(credit_card)

            return Response({
                "message": "Credit card registered with success",
                "card_id": credit_card.id
            })

        except:

            ...


@api_view(["GET"])
def check_single_card(request):
    ...

# class CreditCardViews(APIView):

#     def get(self, request):
#         ...

#     def post(self, request):
#         ...
