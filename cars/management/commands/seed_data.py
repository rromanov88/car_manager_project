from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import random

from cars.models import Car, Tag
from expenses.models import Expense


class Command(BaseCommand):
    help = 'Seed the database with sample cars and expenses'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed data...'))

        # Create tags
        tags_data = ['Family Car', 'Work Vehicle', 'Weekend Car', 'Project Car', 'Daily Driver', 'Sporty', 'Hatchback', 'Enthusiast']
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')

        # Create cars
        cars_data = [
            {
                'make': 'Mazda',
                'model': 'CX-5',
                'year': 2026,
                'fuel_type': 'Gasoline',
                'transmission': 'Automatic',
                'initial_value': 31500.00,
                'current_odometer_reading': 5000,
                'color': 'Soul Red Crystal',
                'license_plate': 'MZD-2026',
                'vin': 'JM3KF1DY7R0123456',
                'description': 'Stylish crossover with a premium interior and agile handling.',
                'tags': ['Work Vehicle','Family Car', 'Daily Driver']
            },
            {
                'make': 'Honda',
                'model': 'Civic',
                'year': 2018,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'initial_value': 18000.00,
                'current_odometer_reading': 100000,
                'color': 'Blue',
                'license_plate': 'XYZ-5678',
                'vin': '2HGFB2F59EH501234',
                'description': 'Compact and reliable car for small families or teenagers.',
                'tags': ['Hatchback', 'Family Car', 'Daily Driver']
            },
            {
                'make': 'Honda',
                'model': 'CR-V',
                'year': 2021,
                'fuel_type': 'Diesel',
                'transmission': 'Automatic',
                'initial_value': 45000.00,
                'current_odometer_reading': 40000,
                'color': 'Black',
                'license_plate': 'TRK-9999',
                'vin': '1FTFW1ET5MFC12345',
                'description': 'Great SUV for bigger families.',
                'tags': ['Work Vehicle', 'Family Car', 'Daily Driver']
            },
            {
                'make': 'Tesla',
                'model': 'Model 3',
                'year': 2022,
                'fuel_type': 'Electric',
                'transmission': 'Automatic',
                'initial_value': 48000.00,
                'current_odometer_reading': 25000,
                'color': 'White',
                'license_plate': 'ELC-2022',
                'vin': '5YJ3E1EA8NF123456',
                'description': 'Modern electric vehicle, great for commuting and families.',
                'tags': ['Daily Driver', 'Family Car']
            },
            {
                'make': 'Volkswagen',
                'model': 'Golf GTI',
                'year': 2026,
                'fuel_type': 'Gasoline',
                'transmission': 'Automatic',
                'initial_value': 35000.00,
                'current_odometer_reading': 15000,
                'color': 'Kings Red Metallic',
                'license_plate': 'GTI-FAST',
                'vin': 'WVWZZZCDZRW123456',
                'description': 'Ultimate performance hatchback blending speed with everyday utility.',
                'tags': ['Sporty', 'Hatchback', 'Enthusiast']
            },

        ]

        cars = []
        for car_data in cars_data:
            tag_names = car_data.pop('tags', [])
            car, created = Car.objects.get_or_create(
                make=car_data['make'],
                model=car_data['model'],
                year=car_data['year'],
                defaults=car_data
            )
            if created:
                # Add tags
                for tag_name in tag_names:
                    tag = Tag.objects.get(name=tag_name)
                    car.tags.add(tag)
                self.stdout.write(f'Created car: {car}')
            cars.append(car)

        # Create expenses
        expense_types = ['Fuel', 'Maintenance', 'Insurance', 'Repair', 'Other']
        expense_descriptions = {
            'Fuel': ['Gas fill-up', 'Premium fuel', 'Diesel refill'],
            'Maintenance': ['Oil change', 'Tire rotation', 'Brake service', 'Air filter replacement'],
            'Insurance': ['Monthly insurance', 'Annual insurance payment', 'Insurance renewal'],
            'Repair': ['Brake pad replacement', 'Battery replacement', 'Transmission repair'],
            'Other': ['Car wash', 'Parking fees', 'Toll fees']
        }

        for car in cars:
            # Create expenses for each car
            num_expenses = random.randint(5, 15)
            base_date = date.today() - timedelta(days=365)
            
            for i in range(num_expenses):
                expense_type = random.choice(expense_types)
                expense_date = base_date + timedelta(days=random.randint(0, 365))
                
                # Set amount based on expense type
                if expense_type == 'Fuel':
                    amount = round(random.uniform(30.00, 80.00), 2)
                elif expense_type == 'Insurance':
                    amount = round(random.uniform(100.00, 500.00), 2)
                elif expense_type == 'Maintenance':
                    amount = round(random.uniform(50.00, 300.00), 2)
                elif expense_type == 'Repair':
                    amount = round(random.uniform(100.00, 1000.00), 2)
                else:
                    amount = round(random.uniform(10.00, 100.00), 2)
                
                description = random.choice(expense_descriptions[expense_type])
                odometer_reading = car.current_odometer_reading - random.randint(0, int(car.current_odometer_reading * 0.4))
                
                Expense.objects.create(
                    car=car,
                    expense_type=expense_type,
                    amount=amount,
                    date=expense_date,
                    description=description,
                    odometer_reading_at_expense=odometer_reading if odometer_reading > 0 else None
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded data!'))
        self.stdout.write(f'Created {len(cars)} cars')
        self.stdout.write(f'Created expenses for all cars')
