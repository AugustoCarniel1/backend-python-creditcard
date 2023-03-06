from django.contrib import admin

from .models import CreditCard


class CreditCardAdmin(admin.ModelAdmin):
    ...


admin.site.register(CreditCard, CreditCardAdmin)
