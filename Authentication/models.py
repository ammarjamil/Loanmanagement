from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import datetime

class User(AbstractUser):
    blacklisted = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

class LoanRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            # Calculate and set the due date based on the current date
            self.due_date = datetime.date.today() + datetime.timedelta(days=7)  # Assuming a week for loan repayment

        super().save(*args, **kwargs)

    # Add any other fields as needed

class LoanApproval(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan Approval: {self.loan_request} - {self.status}"

class Comment(models.Model):
    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()