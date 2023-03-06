from creditcardapi import views
from django.urls import path

# super user
# augusto.carniel
# 123456

# card_identifier
# https://github.com/adelq/card_identifier

urlpatterns = [
    path('api/v1/credit-card/', views.credit_card, name='credit-card'),
    path('api/v1/credit-card/<int:key>/',
         views.credit_card, name='single-credit-card'),
]
