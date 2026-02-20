from datetime import date
from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError

from cars.models import Car, Tag
from cars.validators import year_validator, vin_validator


class CarForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text='Select tags to categorize this car'
    )
    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 2020', 'min': '1900'}),
        validators=[year_validator],
        help_text='Manufacturing year'
    )
    initial_value = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': 'Purchase price'}),
        label='Initial Value (USD)',
        help_text='The price you paid for the car'
    )

    class Meta:
        model = Car
        fields = [
            'make', 'model', 'year', 'fuel_type', 'transmission',
            'initial_value', 'current_mileage', 'color', 'license_plate',
            'vin', 'description', 'tags'
        ]
        exclude = ['slug']
        widgets = {
            'make': forms.TextInput(attrs={'placeholder': 'e.g., Toyota'}),
            'model': forms.TextInput(attrs={'placeholder': 'e.g., Camry'}),
            'color': forms.TextInput(attrs={'placeholder': 'e.g., Red'}),
            'license_plate': forms.TextInput(attrs={'placeholder': 'e.g., ABC-1234'}),
            'vin': forms.TextInput(attrs={'placeholder': '17-character VIN', 'maxlength': '17'}),
            'description': forms.Textarea(attrs={'placeholder': 'Additional details about the car', 'rows': 4}),
            'current_mileage': forms.NumberInput(attrs={'placeholder': 'Current mileage in miles', 'min': '0'}),
            'fuel_type': forms.Select(attrs={'class': 'form-select'}),
            'transmission': forms.Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'make': {'max_length': 'Make must be less than 50 characters'},
            'model': {'max_length': 'Model must be less than 50 characters'},
            'year': {'invalid': 'Please enter a valid year'},
        }

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.helper = FormHelper()
        self.helper.form_id = 'id-carForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_vin(self):
        vin = self.cleaned_data.get('vin')
        if vin:
            vin_validator(vin)
            # Check for duplicate VIN
            qs = Car.objects.filter(vin=vin)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('A car with this VIN already exists.')
        return vin

    def clean_license_plate(self):
        license_plate = self.cleaned_data.get('license_plate')
        if license_plate:
            # Check for duplicate license plate
            qs = Car.objects.filter(license_plate=license_plate)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError('A car with this license plate already exists.')
        return license_plate

    def clean(self):
        cleaned = super().clean()
        year = cleaned.get('year')
        current_mileage = cleaned.get('current_mileage', 0)
        
        # Validate mileage is reasonable for the car's age
        if year and current_mileage:
            current_year = date.today().year
            age = current_year - year
            if age > 0:
                avg_miles_per_year = current_mileage / age
                if avg_miles_per_year > 200000:
                    raise ValidationError({
                        'current_mileage': 'Mileage seems unusually high for a car of this age.'
                    })
        
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class CarCreateForm(CarForm):
    pass


class CarEditForm(CarForm):
    # Make certain fields read-only in edit form
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        # Make VIN read-only if it exists
        if self.instance and self.instance.vin:
            self.fields['vin'].widget.attrs['readonly'] = True
            self.fields['vin'].help_text = 'VIN cannot be changed once set'


class CarDeleteForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year']

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        # Make all fields read-only
        for name in self.fields:
            self.fields[name].disabled = True
            self.fields[name].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_id = 'id-carDeleteForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirm Delete', css_class='btn-danger'))


class CarSearchForm(forms.Form):
    query = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by make, model, or year...', 'class': 'form-control'})
    )
    fuel_type = forms.ChoiceField(
        choices=[('', 'All Fuel Types')] + list(Car.FuelTypeChoices.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    year_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Min year', 'min': '1900', 'class': 'form-control'})
    )
    year_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Max year', 'min': '1900', 'class': 'form-control'})
    )
