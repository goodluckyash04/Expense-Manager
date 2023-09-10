from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Payment)
admin.site.register(Task)
admin.site.register(Loan)
admin.site.register(EMI)
admin.site.register(DeletedEMI)
admin.site.register(DeletePayment)