from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Payment(models.Model):
    category = [
        ("Personal", 'Personal'),
        ("Loan", 'Loan'),
        ("Food", 'Food'),
        ("Shopping", 'Shopping'),
    ]
    payment_type = models.CharField(max_length=50)
    category = models.CharField(max_length=50,choices=category,default="Personal")
    payment_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    amount = models.FloatField(default=0.0)
    payment_for = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    payment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.payment_by.name } {self.payment_type} {self.amount}"



class Task(models.Model):
    priority = models.CharField(max_length=50)
    task_title = models.CharField(max_length=50)
    complete_by = models.DateTimeField(auto_now=False, auto_now_add=False)
    task_detail = models.CharField(max_length=250)
    status = models.CharField(max_length=50)
    completed_on = models.DateTimeField(auto_now=False, auto_now_add=False,default=None)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.task_title
    
class Loan(models.Model):
    title = models.CharField(max_length=50)
    amount = models.FloatField(default=0.0)
    started_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.title


class EMI(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    note = models.CharField(max_length=100,default=None)
    paid_on = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.loan.title

