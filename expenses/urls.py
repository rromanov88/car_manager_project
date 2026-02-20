from django.urls import path
from expenses.views import expenses_list, expense_detail, expense_create, expense_edit, expense_delete

app_name = 'expenses'

urlpatterns = [
    path('', expenses_list, name='list'),
    path('create/', expense_create, name='create'),
    path('<int:pk>/', expense_detail, name='detail'),
    path('<int:pk>/edit/', expense_edit, name='edit'),
    path('<int:pk>/delete/', expense_delete, name='delete'),
]
