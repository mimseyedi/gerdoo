from django.urls import path

# Pages
from .views.pages import (
    home,
)
# Authenticating
from .views.auth import (
    login_view,
    logout_view,
)
# Dashboard
from .views.dashboard import (
    dashboard,
    monthly_data_api,
    get_annual_chart_data,
    category_tag_report_api,
)
# Transactions
from .views.transactions import (
    transactions,
    add_transaction,
    delete_transaction,
    get_categories_by_kind,
    get_transactions_by_month,
    get_transaction_details_by_id,
)
# Categories
from .views.categories import (
    categories,
    get_filtered_categories_ajax,
    add_category_ajax,
    get_category_transactions_ajax,
)


urlpatterns = [
    # Home
    path('', home, name="home"),

    # Authenticating
    path('login', login_view, name="login"),
    path('logout', logout_view, name='logout'),

    # Dashboard
    path('dashboard', dashboard, name="dashboard"),
    path('api/monthly-data/', monthly_data_api, name='monthly_data_api'),
    path('api/annual-data/', get_annual_chart_data, name='get_annual_chart_data'),
    path('api/reports/category_tags/', category_tag_report_api, name='category_tag_report_api'),

    # Transactions
    path('transactions', transactions, name="transactions"),
    path('transactions/add/', add_transaction, name='add_transaction'),
    path('transactions/delete/', delete_transaction, name='delete_transaction'),
    path('get_categories/', get_categories_by_kind, name='get_categories_by_kind'),
    path('transactions/details/', get_transaction_details_by_id, name='get_transaction_details'),
    path('transactions/get_by_month/', get_transactions_by_month, name='get_transactions_by_month'),

    # Categories
    path('categories', categories, name='categories'),
    path('categories/data/', get_filtered_categories_ajax, name='get_filtered_categories_ajax'),
    path('categories/add/', add_category_ajax, name='add_category_ajax'),
    path('categories/transactions/data/', get_category_transactions_ajax, name='get_category_transactions_ajax'),
]