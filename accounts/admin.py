from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(FinancialProduct)
admin.site.register(Task)
admin.site.register(LedgerTransaction)
admin.site.register(Reminder)
