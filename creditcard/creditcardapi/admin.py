from django.contrib import admin

from .models import CreditCardBrand, CreditCardModel


class CreditCardBrandAdmin(admin.ModelAdmin):
    ...


admin.site.register(CreditCardBrand, CreditCardBrandAdmin)


class CreditCardAdmin(admin.ModelAdmin):
    ...


admin.site.register(CreditCardModel, CreditCardAdmin)
