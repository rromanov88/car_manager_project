from django.db.models import Q, Sum, Count, Avg
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from cars.forms import CarForm, CarCreateForm, CarEditForm, CarDeleteForm, CarSearchForm
from cars.models import Car, Tag


def handler404(request, exception):
    """Custom 404 handler"""
    return render(request, '404.html', status=404)


def landing_page(request: HttpRequest) -> HttpResponse:
    """Landing page with statistics and recent cars"""
    total_cars = Car.objects.count()
    total_expenses = Car.objects.aggregate(
        total=Sum('expenses__amount')
    )['total'] or 0
    
    recent_cars = Car.objects.select_related().prefetch_related('tags', 'expenses')[:6]
    cars_with_expenses = Car.objects.annotate(
        expense_count=Count('expenses')
    ).filter(expense_count__gt=0).order_by('-expense_count')[:5]

    context = {
        'total_cars': total_cars,
        'total_expenses': total_expenses,
        'recent_cars': recent_cars,
        'cars_with_expenses': cars_with_expenses,
        'page_title': 'Car Manager - Home',
    }
    return render(request, 'cars/landing_page.html', context)


def cars_list(request: HttpRequest) -> HttpResponse:
    """List all cars with search and filter functionality"""
    search_form = CarSearchForm(request.GET or None)
    
    cars = Car.objects.annotate(
        total_expenses=Sum('expenses__amount'),
        expense_count=Count('expenses')
    ).prefetch_related('tags').order_by('-year', 'make', 'model')

    if request.GET:
        if search_form.is_valid():
            query = search_form.cleaned_data.get('query')
            fuel_type = search_form.cleaned_data.get('fuel_type')
            year_min = search_form.cleaned_data.get('year_min')
            year_max = search_form.cleaned_data.get('year_max')

            if query:
                cars = cars.filter(
                    Q(make__icontains=query) |
                    Q(model__icontains=query) |
                    Q(year__icontains=query)
                )
            
            if fuel_type:
                cars = cars.filter(fuel_type=fuel_type)
            
            if year_min:
                cars = cars.filter(year__gte=year_min)
            
            if year_max:
                cars = cars.filter(year__lte=year_max)

    # Pagination
    paginator = Paginator(cars, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cars': page_obj,
        'search_form': search_form,
        'page_title': 'Cars List',
    }
    return render(request, 'cars/list.html', context)


def car_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Display car details with expenses"""
    car = get_object_or_404(
        Car.objects.prefetch_related('tags', 'expenses'),
        slug=slug
    )
    
    # Get expenses for this car
    expenses = car.expenses.all().order_by('-date', '-created_at')
    
    # Calculate statistics
    expense_stats = car.expenses.aggregate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount')
    )
    
    # Group expenses by type
    expenses_by_type = car.expenses.values('expense_type').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')

    context = {
        'car': car,
        'expenses': expenses[:10],  # Show last 10 expenses
        'expense_stats': expense_stats,
        'expenses_by_type': expenses_by_type,
        'page_title': f'{car} Details',
    }
    return render(request, 'cars/detail.html', context)


def car_create(request: HttpRequest) -> HttpResponse:
    """Create a new car"""
    form = CarCreateForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        if form.is_valid():
            car = form.save()
            return redirect('cars:detail', slug=car.slug)
    
    context = {
        'form': form,
        'page_title': 'Add New Car',
    }
    return render(request, 'cars/create.html', context)


def car_edit(request: HttpRequest, pk: int) -> HttpResponse:
    """Edit an existing car"""
    car = get_object_or_404(Car, pk=pk)
    form = CarEditForm(request.POST or None, request.FILES or None, instance=car)
    
    if request.method == 'POST':
        if form.is_valid():
            car = form.save()
            return redirect('cars:detail', slug=car.slug)
    
    context = {
        'form': form,
        'car': car,
        'page_title': f'Edit {car}',
    }
    return render(request, 'cars/edit.html', context)


def car_delete(request: HttpRequest, pk: int) -> HttpResponse:
    """Delete a car with confirmation"""
    car = get_object_or_404(Car, pk=pk)
    form = CarDeleteForm(request.POST or None, instance=car)
    
    if request.method == 'POST':
        if form.is_valid():
            car.delete()
            return redirect('cars:list')
    
    context = {
        'form': form,
        'car': car,
        'page_title': f'Delete {car}',
    }
    return render(request, 'cars/delete.html', context)
