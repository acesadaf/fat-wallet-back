from django.urls import path

from backend.views import graphs, cat_exp_section, signin, expense_table


urlpatterns = [
    # path("", views.index, name="index"),
    path("add_user", signin.add_user, name="add_user"),
    path("sign_in", signin.sign_in, name="sign_in"),
    path("expense_submit", cat_exp_section.expense_submit, name="expense_submit"),
    path("category_submit", cat_exp_section.category_submit, name="category_submit"),
    path("expense_data", expense_table.expense_data, name="expense_data"),
    path("category_data", cat_exp_section.category_data, name="category_data"),
    path("category_wise_user_data", graphs.category_wise_user_data,
         name="category_wise_user_data"),
    path("monthly_user_data", graphs.monthly_user_data,
         name="monthly_user_data"),
    path("category_delete", cat_exp_section.category_delete, name="category_delete"),
    path("category_edit", cat_exp_section.category_edit, name="category_edit"),
    path('expense_delete', expense_table.expense_delete, name="expense_delete"),
    path('expense_edit', expense_table.expense_edit, name="expense_edit"),
]
