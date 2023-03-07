from .views import CreditCardView, CreditCardList, CustomAuthToken, generate_keys
from django.urls import path

# super user
# augusto.carniel
# 123456

#db1affdd21aa4f41325aaf2347faf89597fbcf88


#another libs
#django-crispy-forms-2.0
#httpie

urlpatterns = [
    path('api/v1/credit-card', CreditCardView.as_view()),
    path('api/v1/credit-card/list', CreditCardList.as_view()),
    path('api/v1/credit-card/<int:key>',
         CreditCardView.as_view()),
    path('api/v1/generate-key', generate_keys, name='generate-keys'),
    path('api/v1/token/auth', CustomAuthToken.as_view())    
]