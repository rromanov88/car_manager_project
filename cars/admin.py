from django.contrib import admin
from cars.models import Car, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'year', 'fuel_type', 'current_mileage', 'initial_value']
    list_filter = ['fuel_type', 'transmission', 'year']
    search_fields = ['make', 'model', 'license_plate', 'vin']
    prepopulated_fields = {'slug': ('make', 'model', 'year')}
    filter_horizontal = ['tags']
    readonly_fields = ['created_at', 'updated_at']
