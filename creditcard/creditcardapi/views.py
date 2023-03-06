from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_500_INTERNAL_SERVER_ERROR)

from creditcard import CreditCard

from .exception import *
from .models import CreditCardModel
from .serializer import CreditCardSerializer


@api_view(["GET", "POST"])
def credit_card(request):

    if request.method == "GET":

        try:

            card_list = CreditCardModel.objects.all()

            serializer = CreditCardSerializer(card_list, many=True)

            return Response({
                "credit_card_list": serializer.data
            }, status=HTTP_200_OK)

        except:

            return Response({
                "message": "Error 5XX"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    else:

        try:

            params = request.data

            cc = CreditCard(params["number"])

            if not cc.is_valid():
                raise InvalidCreditCardNumberException

            expiration_date = datetime.strftime()

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

        except InvalidCreditCardNumberException:
            return Response({
                "message": "Invalid Credit Card Number"
            }, status=HTTP_400_BAD_REQUEST)

        except InvalidDateException:
            return Response({
                "message": "Invalid Expiration Date"
            }, status=HTTP_400_BAD_REQUEST)

        except:

            ...


@ api_view(["GET"])
def check_single_card(request):
    ...

# class CreditCardViews(APIView):

#     def get(self, request):
#         ...

#     def post(self, request):
#         ...
