from django.contrib import admin
from expenses.models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['car', 'expense_type', 'amount', 'date', 'created_at']
    list_filter = ['expense_type', 'date']
    search_fields = ['car__make', 'car__model', 'description']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
