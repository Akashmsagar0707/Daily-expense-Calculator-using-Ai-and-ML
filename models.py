from django.db import models

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Utilities', 'Utilities'),
        ('Entertainment', 'Entertainment'),
        ('Others', 'Others'),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"


