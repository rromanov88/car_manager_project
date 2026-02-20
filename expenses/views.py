from django.db.models import Q, Sum, Count, Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from expenses.forms import ExpenseForm, ExpenseCreateForm, ExpenseEditForm, ExpenseDeleteForm, ExpenseFilterForm
from expenses.models import Expense


def expenses_list(request: HttpRequest) -> HttpResponse:
    """List all expenses with filtering"""
    filter_form = ExpenseFilterForm(request.GET or None)
    
    expenses = Expense.objects.select_related('car').order_by('-date', '-created_at')

    if request.GET:
        if filter_form.is_valid():
            car = filter_form.cleaned_data.get('car')
            expense_type = filter_form.cleaned_data.get('expense_type')
            date_from = filter_form.cleaned_data.get('date_from')
            date_to = filter_form.cleaned_data.get('date_to')

            if car:
                expenses = expenses.filter(car=car)
            
            if expense_type:
                expenses = expenses.filter(expense_type=expense_type)
            
            if date_from:
                expenses = expenses.filter(date__gte=date_from)
            
            if date_to:
                expenses = expenses.filter(date__lte=date_to)

    # Pagination
    paginator = Paginator(expenses, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate totals
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'expenses': page_obj,
        'filter_form': filter_form,
        'total_amount': total_amount,
        'page_title': 'Expenses List',
    }
    return render(request, 'expenses/list.html', context)


def expense_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Display expense details"""
    expense = get_object_or_404(Expense.objects.select_related('car'), pk=pk)
    
    # Get related expenses for the same car
    related_expenses = Expense.objects.filter(
        car=expense.car
    ).exclude(pk=pk).order_by('-date')[:5]

    context = {
        'expense': expense,
        'related_expenses': related_expenses,
        'page_title': f'Expense Details - {expense.expense_type}',
    }
    return render(request, 'expenses/detail.html', context)


def expense_create(request: HttpRequest) -> HttpResponse:
    """Create a new expense"""
    form = ExpenseCreateForm(request.POST or None, request.FILES or None)
    
    # Pre-select car if provided in query string
    car_id = request.GET.get('car')
    if car_id and not request.POST:
        try:
            from cars.models import Car
            car = Car.objects.get(pk=car_id)
            form.fields['car'].initial = car
        except Car.DoesNotExist:
            pass
    
    if request.method == 'POST':
        if form.is_valid():
            expense = form.save()
            return redirect('expenses:detail', pk=expense.pk)
    
    context = {
        'form': form,
        'page_title': 'Add New Expense',
    }
    return render(request, 'expenses/create.html', context)


def expense_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Edit an existing expense"""
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseEditForm(request.POST or None, request.FILES or None, instance=expense)
    
    if request.method == 'POST':
        if form.is_valid():
            expense = form.save()
            return redirect('expenses:detail', pk=expense.pk)
    
    context = {
        'form': form,
        'expense': expense,
        'page_title': f'Edit Expense - {expense.expense_type}',
    }
    return render(request, 'expenses/edit.html', context)


def expense_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete an expense with confirmation"""
    expense = get_object_or_404(Expense, pk=pk)
    form = ExpenseDeleteForm(request.POST or None, instance=expense)
    
    if request.method == 'POST':
        if form.is_valid():
            car = expense.car
            expense.delete()
            return redirect('cars:detail', slug=car.slug)
    
    context = {
        'form': form,
        'expense': expense,
        'page_title': f'Delete Expense - {expense.expense_type}',
    }
    return render(request, 'expenses/delete.html', context)
