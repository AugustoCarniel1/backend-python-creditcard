from datetime import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from creditcard.exceptions import BrandNotFound

from .exception import *


def basic_info_verifier(params, credit_card):

    if not credit_card.is_valid():
        raise InvalidCreditCardNumberException

    try:

        brand = credit_card.get_brand()

    except:

        raise BrandNotFound

    try:

        expiration_date = datetime.strptime(
            params["exp_date"], "%m/%Y")

        if expiration_date < datetime.now():

            raise InvalidDateException

        else:

            expiration_date.strftime("%m/%d/%Y")

    except:

        raise InvalidDateException

    return {
        'brand': brand,
        'expiration_date': expiration_date
    }


def read_keys(type):

    if type == "public":

        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        return public_key

    else:

        with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        return private_key
