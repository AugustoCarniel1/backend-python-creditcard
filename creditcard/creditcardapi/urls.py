from django.urls import path

from .views import (CreditCardList, CreditCardView, CustomAuthToken,
                    generate_keys)

urlpatterns = [
    path('api/v1/credit-card', CreditCardView.as_view()),
    path('api/v1/credit-card/list', CreditCardList.as_view()),
    path('api/v1/credit-card/<int:key>',
         CreditCardView.as_view()),
    path('api/v1/generate-key', generate_keys, name='generate-keys'),
    path('api/v1/token/auth', CustomAuthToken.as_view())
]
