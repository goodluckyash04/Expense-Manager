from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class FinancialProduct(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    no_of_installments = models.IntegerField(default=0)
    started_on = models.DateField()
    status = models.CharField(max_length=20, choices=[("Open", _("Open")), ("Closed", _("Closed"))], default="Open")
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Financial Product")
        verbose_name_plural = _("Financial Products")


class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ("Personal", _('Personal')),
        ("Loan", _('Loan')),
        ("Food", _('Food')),
        ("Shopping", _('Shopping')),
    ]
    STATUS_CHOICES = [
        ("Completed", _("Completed")),
        ("Pending", _("Pending")),
    ]
    MODE_CHOICES = [
        ("CreditCard", _("CreditCard")),
        ("Online", _("Online")),
        ("Cash", _("Cash")),
    ]
    type = models.CharField(max_length=50)  # type is a reserved keyword, consider renaming this field
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Personal")
    date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    beneficiary = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    source = models.ForeignKey(FinancialProduct, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True, default=None)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, null=True)
    mode_detail = models.CharField(max_length=10,null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("Low", _("Low")),
        ("Medium", _("Medium")),
        ("High", _("High")),
    ]
    STATUS_CHOICES = [
        ("Pending", _("Pending")),
        ("Completed", _("Completed")),
    ]

    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, blank=True)
    name = models.CharField(max_length=100)
    complete_by_date = models.DateField()
    description = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    completed_on = models.DateField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
