from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify
from django.urls import reverse

from common.models import TimeStampModel
from cars.validators import year_validator, vin_validator


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # cars = models.ManyToManyField('Car', related_name='tags', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Car(TimeStampModel):
    class FuelTypeChoices(models.TextChoices):
        PETROL = 'Petrol', 'Petrol'
        DIESEL = 'Diesel', 'Diesel'
        ELECTRIC = 'Electric', 'Electric'
        HYBRID = 'Hybrid', 'Hybrid'

    class TransmissionChoices(models.TextChoices):
        MANUAL = 'Manual', 'Manual'
        AUTOMATIC = 'Automatic', 'Automatic'
        CVT = 'CVT', 'CVT'

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FuelTypeChoices.choices, default=FuelTypeChoices.PETROL)
    transmission = models.CharField(max_length=20, choices=TransmissionChoices.choices, default=TransmissionChoices.MANUAL)
    initial_value = models.DecimalField(max_digits=10, decimal_places=2, help_text='Initial purchase value in USD')
    current_mileage = models.PositiveIntegerField(default=0, help_text='Current mileage in miles')
    color = models.CharField(max_length=30, blank=True)
    license_plate = models.CharField(max_length=20, unique=True, blank=True, null=True)
    vin = models.CharField(max_length=17, unique=True, blank=True, null=True, validators=[vin_validator], help_text='Vehicle Identification Number')
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    tags = models.ManyToManyField('Tag', related_name='cars', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.make}-{self.model}-{self.year}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.year} {self.make} {self.model}'

    def get_absolute_url(self):
        return reverse('cars:detail', kwargs={'slug': self.slug})

    def total_expenses(self):
        """Calculate total expenses for this car"""
        return self.expenses.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    def total_maintenance_cost(self):
        """Calculate total maintenance expenses"""
        return self.expenses.filter(expense_type='Maintenance').aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    def total_fuel_cost(self):
        """Calculate total fuel expenses"""
        return self.expenses.filter(expense_type='Fuel').aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    def total_insurance_cost(self):
        """Calculate total insurance expenses"""
        return self.expenses.filter(expense_type='Insurance').aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    class Meta:
        ordering = ['-year', 'make', 'model']
        unique_together = ['make', 'model', 'year', 'vin']
