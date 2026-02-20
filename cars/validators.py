from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    """Validate that year is not in the future and reasonable"""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(f'Year cannot be in the future. Current year is {current_year}.')
    if value < 1900:
        raise ValidationError('Year must be 1900 or later.')


def vin_validator(value):
    """Validate VIN format (17 characters, alphanumeric)"""
    if value:
        if len(value) != 17:
            raise ValidationError('VIN must be exactly 17 characters long.')
        if not value.isalnum():
            raise ValidationError('VIN must contain only letters and numbers.')
