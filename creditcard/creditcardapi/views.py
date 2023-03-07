from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_500_INTERNAL_SERVER_ERROR)

from creditcard import CreditCard
from creditcard.exceptions import BrandNotFound

from .exception import *
from .models import CreditCardBrand, CreditCardModel
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

            credit_card = CreditCard(params["number"])

            if not credit_card.is_valid():
                raise InvalidCreditCardNumberException

            try:

                brand = credit_card.get_brand()

            except:

                raise BrandNotFound

            try:

                expiration_date = datetime.strptime(
                    params["exp_date"], "%m/%Y").strftime()

                if expiration_date < datetime.now():

                    raise InvalidDateException

            except:

                raise InvalidDateException

            brand_obj = CreditCardBrand.objects.get(description=brand)

            credit_card = CreditCardModel(
                exp_date=expiration_date,
                holder=params["holder"],
                number=params["number"],
                cvv=params["cvv"] if params["cvv"] else "",
                brand=brand_obj
            )

            credit_card.save()

            serializer = CreditCardSerializer(credit_card)

            return Response({
                "message": "Credit card registered with success",
                "card_id": credit_card.id
            })

        except BrandNotFound:
            return Response({
                "message": "Brand Not Found"
            }, status=HTTP_400_BAD_REQUEST)

        except InvalidCreditCardNumberException:
            return Response({
                "message": "Invalid Credit Card Number"
            }, status=HTTP_400_BAD_REQUEST)

        except InvalidDateException:
            return Response({
                "message": "Invalid Expiration Date, must be later than now and valid"
            }, status=HTTP_400_BAD_REQUEST)

        except InvalidHolderException:
            return Response({
                "message": "Invalid Holder Name, must have at least 2 characters"
            }, status=HTTP_400_BAD_REQUEST)

        except:

            return Response({
                "message": "Error, code failed at card creation"
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)


@ api_view(["GET"])
def check_single_card(request, key):

    print(key)

    credit_card = CreditCardModel.objects.get(pk=key)

    serializer = CreditCardSerializer(credit_card)

    return Response({
        "credit_card": serializer.data
    }, status=HTTP_200_OK)

# class CreditCardViews(APIView):

#     def get(self, request):
#         ...

#     def post(self, request):
#         ...
