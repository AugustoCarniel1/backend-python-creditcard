from datetime import date, timedelta

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)

from .models import CreditCardBrand, CreditCardModel
from .views import CreditCardList, CreditCardView


class CreditCardTestCase(APITestCase):

    def setUp(self):

        # Create main request
        self.factory = APIRequestFactory()
        self.view = CreditCardView.as_view()

        self.factory_list = APIRequestFactory()
        self.view_list = CreditCardList.as_view()

        self.user = User.objects.create_superuser(username='test.case',
                                                  email='test.case@gmail.com',
                                                  password='123456')

        if self.user is not None:

            try:

                self.token = Token.objects.get(user=self.user)

            except:

                self.token = Token.objects.create(user=self.user)

            self.headers = {'Authorization': 'Token ' + self.token.key}

    def test_credit_card_with_invalid_number(self):

        request = self.factory.put('/api/v1/credit-card', {
            'exp_date': '02/2028',
            'holder': 'Olivia Johnson',
            'number': '1234567891231234',
            'cvv': '999'
        }, **self.headers)

        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertDictEqual({
            'message': 'Invalid Credit Card Number'
        }, response.data)

    def test_credit_card_with_date_before_today(self):

        request = self.factory.put('/api/v1/credit-card', {
            'exp_date': '02/2021',
            'holder': 'Olivia Johnson',
            'number': '5544617035307084',
            'cvv': '999'
        }, **self.headers)

        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertDictEqual({
            'message': 'Invalid Expiration Date, must be later than now and valid'
        }, response.data)

    def test_credit_card_with_invalid_date(self):

        request = self.factory.put('/api/v1/credit-card', {
            'exp_date': '13/2021',
            'holder': 'Olivia Johnson',
            'number': '5544617035307084',
            'cvv': '999'
        }, **self.headers)

        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertDictEqual({
            'message': 'Invalid Expiration Date, must be later than now and valid'
        }, response.data)

    def test_credit_card_with_missing_information(self):

        request = self.factory.put('/api/v1/credit-card', {
            'exp_date': '13/2021',
            'holder': 'Olivia Johnson',
            'cvv': '999'
        }, **self.headers)

        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertDictEqual({
            'message': 'Error, code failed at card creation'
        }, response.data)

    def test_create_credit_card_visa(self):

        request = self.factory.put('/api/v1/credit-card', {
            'exp_date': '11/2027',
            'holder': 'Alanis Seress',
            'number': '4037934769917104',
            'cvv': '725'
        }, **self.headers)

        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertDictContainsSubset({
            'message': 'Credit card registered with success'
        }, response.data)

    def test_create_credit_card_mastercard(self):

        request = self.factory.put('/api/v1/credit-card', {
            'exp_date': '06/2028',
            'holder': 'Martina Bauelos',
            'number': '5544617035307084',
            'cvv': '592'
        }, **self.headers)

        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertDictContainsSubset({
            'message': 'Credit card registered with success'
        }, response.data)

    def test_create_credit_card_american_express(self):

        request = self.factory.put('/api/v1/credit-card', {
            'exp_date': '07/2026',
            'holder': 'Takiko Luse',
            'number': '340205338109972',
            'cvv': '9299'
        }, **self.headers)

        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertDictContainsSubset({
            'message': 'Credit card registered with success'
        }, response.data)

    def test_get_credit_card_list(self):

        request = self.factory_list.get(
            '/api/v1/credit-card/list', **self.headers)

        force_authenticate(request, self.user)

        response = self.view_list(request)

        self.assertTrue(response.status_code == 200)

    def test_get_single_card_not_found(self):

        request = self.factory.get(
            '/api/v1/credit-card/999', **self.headers)

        force_authenticate(request, self.user)

        response = self.view(request)

        self.assertDictContainsSubset(
            {'message': 'The specified card does not exist'}, response.data)
