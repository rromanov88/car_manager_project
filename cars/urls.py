from django.urls import path, include
from cars.views import landing_page, cars_list, car_detail, car_create, car_edit, car_delete

app_name = 'cars'

cars_patterns = [
    path('', cars_list, name='list'),
    path('create/', car_create, name='create'),
    path('<int:pk>/', include([
        path('edit/', car_edit, name='edit'),
        path('delete/', car_delete, name='delete'),
    ])),
    path('<slug:slug>/', car_detail, name='detail'),
]

urlpatterns = [
    path('', landing_page, name='home'),
    path('cars/', include(cars_patterns)),
]
