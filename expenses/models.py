from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

from common.models import TimeStampModel


class Expense(TimeStampModel):
    class ExpenseTypeChoices(models.TextChoices):
        FUEL = 'Fuel', 'Fuel'
        MAINTENANCE = 'Maintenance', 'Maintenance'
        INSURANCE = 'Insurance', 'Insurance'
        REPAIR = 'Repair', 'Repair'
        OTHER = 'Other', 'Other'

    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=20, choices=ExpenseTypeChoices.choices, default=ExpenseTypeChoices.OTHER)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='Amount must be greater than 0')],
        help_text='Expense amount in USD'
    )
    date = models.DateField()
    description = models.TextField(blank=True, help_text='Additional details about the expense')
    mileage_at_expense = models.PositiveIntegerField(null=True, blank=True, help_text='Car mileage when expense occurred')
    receipt_image = models.ImageField(upload_to='expense_receipts/', blank=True, null=True)

    def __str__(self):
        return f'{self.expense_type} - ${self.amount} - {self.car}'

    def get_absolute_url(self):
        return reverse('expenses:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['expense_type']),
        ]
