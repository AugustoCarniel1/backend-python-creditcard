# Cryptography API
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
# Django
from django.core.exceptions import ObjectDoesNotExist
# RestFrameWork
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView

# Credit Card API
from creditcard import CreditCard
from creditcard.exceptions import BrandNotFound

# Own project files
from .exception import *
from .helpers import basic_info_verifier, read_keys
from .models import CreditCardBrand, CreditCardModel
from .serializer import CreditCardSerializer
from .utils import encrypt_credit_card_number


@api_view(['POST'])
def generate_keys(request):

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    with open('private_key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open('public_key.pem', 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return Response({
        'message': 'Keys generated with success'
    }, status=HTTP_200_OK)


class CreditCardView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, key=None):

        try:

            # Check for unit test
            if not key and 'key' in request.query_params:
                key = request.query_params['key']

            credit_card = CreditCardModel.objects.get(pk=key)

            serializer = CreditCardSerializer(credit_card)

            return Response({
                'message': 'Credit card information successfully listed',
                'credit_card': serializer.data
            }, status=HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({
                'message': 'The specified card does not exist'
            }, status=HTTP_404_NOT_FOUND)

        except:
            return Response({
                'message': 'Error, cannot list the informations'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):

        try:

            params = request.data

            credit_card = CreditCard(params['number'])

            response = basic_info_verifier(params, credit_card)

            # Create a brand if it doesn't registered in db
            try:
                brand_obj = CreditCardBrand.objects.get(
                    description__icontains=response['brand'])
            except:
                brand_obj = CreditCardBrand.objects.create(
                    description=response['brand'])

            public_key = read_keys('public')

            encrypted_number = encrypt_credit_card_number(
                public_key, params['number'])

            credit_card = CreditCardModel(
                exp_date=response['expiration_date'],
                holder=params['holder'],
                number=encrypted_number,
                cvv=params['cvv'] if params['cvv'] else '',
                brand=brand_obj
            )

            credit_card.save()

            return Response({
                'message': 'Credit card registered with success',
                'card_id': credit_card.id
            }, status=HTTP_201_CREATED)

        except BrandNotFound:
            return Response({
                'message': 'Brand Not Found'
            }, status=HTTP_400_BAD_REQUEST)

        except InvalidCreditCardNumberException:
            return Response({
                'message': 'Invalid Credit Card Number'
            }, status=HTTP_400_BAD_REQUEST)

        except InvalidDateException:
            return Response({
                'message': 'Invalid Expiration Date, must be later than now and valid'
            }, status=HTTP_400_BAD_REQUEST)

        except InvalidHolderException:
            return Response({
                'message': 'Invalid Holder Name, must have at least 2 characters'
            }, status=HTTP_400_BAD_REQUEST)

        except:
            return Response({
                'message': 'Error, code failed at card creation'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)


class CreditCardList(APIView):

    # Garants all the function an auth
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:

            card_list = CreditCardModel.objects.all()

            serializer = CreditCardSerializer(card_list, many=True)

            return Response({
                'message': 'List of credit cards successfully listed',
                'credit_card_list': serializer.data
            }, status=HTTP_200_OK)

        except:
            return Response({
                'message': 'Error, Cannot list all cards'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
