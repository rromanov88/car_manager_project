from datetime import date
from typing import Any

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError

from expenses.models import Expense


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'max': str(date.today())}),
        help_text='Date when the expense occurred'
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00', 'min': '0.01'}),
        label='Amount (USD)',
        help_text='Expense amount'
    )
    mileage_at_expense = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Optional: mileage when expense occurred', 'min': '0'}),
        help_text='Car mileage at the time of expense (optional)'
    )

    class Meta:
        model = Expense
        fields = ['car', 'expense_type', 'amount', 'date', 'description', 'mileage_at_expense', 'receipt_image']
        widgets = {
            'car': forms.Select(attrs={'class': 'form-select'}),
            'expense_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'placeholder': 'Additional details about this expense', 'rows': 3}),
            'receipt_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
        error_messages = {
            'amount': {
                'min_value': 'Amount must be greater than 0',
                'invalid': 'Please enter a valid amount'
            },
            'date': {
                'invalid': 'Please enter a valid date'
            }
        }

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        # Order cars by make and model
        self.fields['car'].queryset = self.fields['car'].queryset.order_by('make', 'model', 'year')
        self.helper = FormHelper()
        self.helper.form_id = 'id-expenseForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_date(self):
        expense_date = self.cleaned_data.get('date')
        if expense_date:
            if expense_date > date.today():
                raise ValidationError('Expense date cannot be in the future.')
        return expense_date

    def clean_mileage_at_expense(self):
        mileage = self.cleaned_data.get('mileage_at_expense')
        car = self.cleaned_data.get('car')
        
        if mileage is not None and car:
            if mileage < 0:
                raise ValidationError('Mileage cannot be negative.')
            # Warn if mileage is less than car's current mileage (but allow it for historical data)
            if mileage > car.current_mileage:
                # This is okay - might be updating mileage
                pass
        return mileage

    def clean(self):
        cleaned = super().clean()
        car = cleaned.get('car')
        mileage_at_expense = cleaned.get('mileage_at_expense')
        expense_date = cleaned.get('date')
        
        if car and mileage_at_expense and expense_date:
            # If mileage is provided, it should be reasonable
            if mileage_at_expense > car.current_mileage:
                # Allow if it's a recent expense and we're updating mileage
                pass
        
        return cleaned


class ExpenseCreateForm(ExpenseForm):
    pass


class ExpenseEditForm(ExpenseForm):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        # Make car read-only in edit form
        if self.instance and self.instance.car:
            self.fields['car'].disabled = True
            self.fields['car'].widget.attrs['readonly'] = True
            self.fields['car'].help_text = 'Car cannot be changed after creation'


class ExpenseDeleteForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['car', 'expense_type', 'amount', 'date']

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        # Make all fields read-only
        for name in self.fields:
            self.fields[name].disabled = True
            self.fields[name].widget.attrs['readonly'] = True

        self.helper = FormHelper()
        self.helper.form_id = 'id-expenseDeleteForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Confirm Delete', css_class='btn-danger'))


class ExpenseFilterForm(forms.Form):
    car = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='All Cars'
    )
    expense_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Expense.ExpenseTypeChoices.choices),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='From Date'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='To Date'
    )

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        from cars.models import Car
        self.fields['car'].queryset = Car.objects.all().order_by('make', 'model')
