from django.contrib import admin
from django.urls import path,include
from expenses import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', views.expense_list, name='expense_list'),
    path('add/', views.add_expense, name='add_expense'),
    # Remove this line because it's already in expenses.urls
    # path('analysis/', views.expense_analysis, name='expense_analysis'),
    path('expenses/', include('expenses.urls')),
    path('delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    

]


