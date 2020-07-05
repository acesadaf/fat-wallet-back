from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_user", views.add_user, name="add_user"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("expense_submit", views.expense_submit, name="expense_submit"),
    path("category_submit", views.category_submit, name="category_submit"),
    path("expense_data", views.expense_data, name="expense_data"),
    path("category_data", views.category_data, name="category_data"),
]
