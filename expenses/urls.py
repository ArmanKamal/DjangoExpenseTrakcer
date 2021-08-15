from django.urls import path
from .views import index,add_expense,create_expense,edit_expense,delete_expense,update_expense,search_expenses,expense_summary,stats_view,expense_export_csv,expense_summary_one_month,expense_export_excel

urlpatterns = [
    path('', index,name="home"),
    path('add-expense', add_expense,name="add-expense"),
    path('create-expense', create_expense,name="create-expense"),
    path('edit-expense/<int:id>', edit_expense,name="edit-expense"),
    path('update-expense/<int:id>', update_expense,name="update-expense"),
    path('delete-expense/<int:id>',delete_expense,name="delete-expense"),
    path('expenses/search/',search_expenses,name="search-expenses"),
    path('expense_category_summary',expense_summary,name="expense_summary"),
    path('expense_category_one_month',expense_summary_one_month,name="expense_summary_one_month"),
    path('expense_export_csv',expense_export_csv,name="expense_export_csv"),
    path('expense_export_excel',expense_export_excel,name="expense_export_excel"),
    path('expenses_stats',stats_view,name="summary")
]
