# Car Manager - Django Web Application

A Django web application for managing your vehicle fleet and tracking expenses. This application allows you to keep detailed records of your cars, monitor expenses (fuel, maintenance, insurance, repairs) and spending patterns.

## Features

- **Car Management**: Add, edit, delete, and view detailed information about your vehicles
- **Expense Tracking**: Record and categorize expenses (Fuel, Maintenance, Insurance, Repairs, Other)
- **Search & Filter**: Search cars by make, model, year, and filter expenses by type, date, and car
- **Statistics**: View expense summaries and statistics for each vehicle
- **Tag System**: Categorize cars with tags (Family Car, Work Vehicle, Weekend Car, etc.)
- **Responsive Design**: Modern Bootstrap 5 interface that works on all devices

## Project Structure

```
car_manager_project/
├── car_manager/          # Main project settings
├── cars/                 # Cars app
│   ├── models.py        # Car and Tag models
│   ├── views.py         # Car views (CRUD operations)
│   ├── forms.py         # Car forms with validations
│   ├── urls.py          # Car URL patterns
│   └── management/      # Management commands
│       └── commands/
│           └── seed_data.py  # Seed data command
├── expenses/            # Expenses app
│   ├── models.py       # Expense model
│   ├── views.py        # Expense views (CRUD operations)
│   ├── forms.py        # Expense forms with validations
│   └── urls.py         # Expense URL patterns
├── common/             # Common app
│   └── models.py       # TimeStampModel (abstract base)
├── templates/          # HTML templates
│   ├── common/         # Base template
│   ├── cars/           # Car templates
│   └── expenses/       # Expense templates
├── staticfiles/        # Static files (CSS, JS, images)
├── media/              # Media files (uploaded images)
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Requirements

- Python 3.11+
- PostgreSQL 12+
- pip (Python package manager)

## Installation & Setup

### 1. Clone or Download the Project

Navigate to the project directory:
```bash
cd car_manager_project
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Setup

#### Create PostgreSQL Database

1. Open PostgreSQL and create a new database:
```sql
CREATE DATABASE car_manager;
```

2. Update database credentials in `car_manager/settings.py` if needed:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'car_manager',
        'USER': 'postgres',        # Change if needed
        'PASSWORD': 'admin',         # Change to your PostgreSQL password
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. (Optional) Load Sample Data

To populate the database with sample cars and expenses:
```bash
python manage.py seed_data
```

### 8. Create Static Files Directory

```bash
mkdir staticfiles
mkdir media
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Environment Variables

The following database credentials are configured in `settings.py`:

- **Database Name**: `car_manager`
- **Database User**: `postgres`
- **Database Password**: `admin`
- **Database Host**: `127.0.0.1`
- **Database Port**: `5432`

**Important**: Update these values in `car_manager/settings.py` to match your PostgreSQL configuration before running migrations.


## Models

### Car Model
- **Fields**: make, model, year, fuel_type, transmission, initial_value, current_mileage, color, license_plate, vin, description, slug
- **Relationships**: Many-to-Many with Tag, One-to-Many with Expense

### Expense Model
- **Fields**: car (ForeignKey), expense_type, amount, date, description, mileage_at_expense, receipt_image
- **Relationships**: Many-to-One with Car

### Tag Model
- **Fields**: name
- **Relationships**: Many-to-Many with Car

## Forms

- **CarForm**: Create/Edit car with comprehensive validations
- **CarDeleteForm**: Confirmation form with read-only fields
- **CarSearchForm**: Search and filter cars
- **ExpenseForm**: Create/Edit expenses with validations
- **ExpenseDeleteForm**: Confirmation form with read-only fields
- **ExpenseFilterForm**: Filter expenses by various criteria

## Validations

### Car Validations
- Year cannot be in the future
- Year must be 1900 or later
- VIN must be exactly 17 alphanumeric characters
- License plate must be unique
- VIN must be unique
- Mileage validation based on car age

### Expense Validations
- Amount must be greater than 0
- Date cannot be in the future
- Mileage cannot be negative

## Templates

The application includes 13+ templates:

1. **Base Template** (`common/base.html`) - Navigation and footer
2. **Landing Page** (`cars/landing_page.html`) - Home with statistics
3. **Cars List** (`cars/list.html`) - List all cars with search
4. **Car Detail** (`cars/detail.html`) - Car details and expenses
5. **Car Create** (`cars/create.html`) - Add new car
6. **Car Edit** (`cars/edit.html`) - Edit car
7. **Car Delete** (`cars/delete.html`) - Delete confirmation
8. **Expenses List** (`expenses/list.html`) - List all expenses
9. **Expense Detail** (`expenses/detail.html`) - Expense details
10. **Expense Create** (`expenses/create.html`) - Add new expense
11. **Expense Edit** (`expenses/edit.html`) - Edit expense
12. **Expense Delete** (`expenses/delete.html`) - Delete confirmation
13. **404 Page** (`404.html`) - Custom error page

## Technologies Used

- **Django 5.2.11** - Web framework
- **PostgreSQL** - Database
- **Bootstrap 5** - Frontend framework
- **Crispy Forms** - Form rendering
- **Pillow** - Image processing

