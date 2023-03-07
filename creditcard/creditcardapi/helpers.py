from datetime import datetime

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
            params["exp_date"], "%m/%Y").strftime()

        if expiration_date < datetime.now():

            raise InvalidDateException

    except:

        raise InvalidDateException

    return {
        'brand': brand,
        'expiration_date': expiration_date
    }
