from django.contrib import admin

from .models import CreditCardModel


class CreditCardAdmin(admin.ModelAdmin):
    ...


admin.site.register(CreditCardModel, CreditCardAdmin)
