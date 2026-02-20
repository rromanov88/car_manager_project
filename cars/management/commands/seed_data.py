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
        tags_data = ['Family Car', 'Work Vehicle', 'Weekend Car', 'Project Car', 'Daily Driver']
        tags = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
            if created:
                self.stdout.write(f'Created tag: {tag_name}')

        # Create cars
        cars_data = [
            {
                'make': 'Toyota',
                'model': 'Camry',
                'year': 2020,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'initial_value': 25000.00,
                'current_mileage': 45000,
                'color': 'Silver',
                'license_plate': 'ABC-1234',
                'vin': '1HGBH41JXMN109186',
                'description': 'Reliable daily driver, well maintained.',
                'tags': ['Family Car', 'Daily Driver']
            },
            {
                'make': 'Honda',
                'model': 'Civic',
                'year': 2018,
                'fuel_type': 'Petrol',
                'transmission': 'Manual',
                'initial_value': 18000.00,
                'current_mileage': 62000,
                'color': 'Blue',
                'license_plate': 'XYZ-5678',
                'vin': '2HGFB2F59EH501234',
                'description': 'Sporty and fun to drive.',
                'tags': ['Weekend Car']
            },
            {
                'make': 'Ford',
                'model': 'F-150',
                'year': 2021,
                'fuel_type': 'Diesel',
                'transmission': 'Automatic',
                'initial_value': 45000.00,
                'current_mileage': 28000,
                'color': 'Black',
                'license_plate': 'TRK-9999',
                'vin': '1FTFW1ET5MFC12345',
                'description': 'Powerful truck for work and towing.',
                'tags': ['Work Vehicle']
            },
            {
                'make': 'Tesla',
                'model': 'Model 3',
                'year': 2022,
                'fuel_type': 'Electric',
                'transmission': 'Automatic',
                'initial_value': 48000.00,
                'current_mileage': 15000,
                'color': 'White',
                'license_plate': 'ELC-2022',
                'vin': '5YJ3E1EA8NF123456',
                'description': 'Modern electric vehicle, great for commuting.',
                'tags': ['Daily Driver', 'Family Car']
            },
            {
                'make': 'BMW',
                'model': '3 Series',
                'year': 2019,
                'fuel_type': 'Petrol',
                'transmission': 'Automatic',
                'initial_value': 35000.00,
                'current_mileage': 55000,
                'color': 'Black',
                'license_plate': 'BMW-2019',
                'vin': 'WBA3A5C59EK123456',
                'description': 'Luxury sedan with great performance.',
                'tags': ['Weekend Car']
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
                mileage = car.current_mileage - random.randint(0, int(car.current_mileage * 0.3))
                
                Expense.objects.create(
                    car=car,
                    expense_type=expense_type,
                    amount=amount,
                    date=expense_date,
                    description=description,
                    mileage_at_expense=mileage if mileage > 0 else None
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded data!'))
        self.stdout.write(f'Created {len(cars)} cars')
        self.stdout.write(f'Created expenses for all cars')
