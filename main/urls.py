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
# Tags
from .views.tags import (
    tags,
    get_all_tags,
    add_tag_ajax,
    delete_tag_ajax,
)
# Cards
from .views.cards import (
    cards,
    add_card,
    activate_card,
    deactivate_card,
)
# Gold
from .views.gold import (
    gold,
    add_gold,
    sell_gold,
)
# Reporting
from .views.reporting import (
    reporting,
    filter_transactions_ajax,
    export_transactions_excel,
)
# Backup
from .views.backup import (
    backup,
    create_backup,
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

    # Tags
    path('tags', tags, name='tags'),
    path('get_all_tags/', get_all_tags, name='get_all_tags'),
    path('tags/add/', add_tag_ajax, name='add_tag_ajax'),
    path('tags/delete/', delete_tag_ajax, name='delete_tag_ajax'),

    # Cards
    path('cards', cards, name='cards'),
    path('cards/add/', add_card, name='add_card'),
    path('cards/activate/', activate_card, name='activate_card'),
    path('cards/deactivate/', deactivate_card, name='deactivate_card'),

    # Gold
    path('gold', gold, name='gold'),
    path('gold/add', add_gold, name='add_gold'),
    path('gold/sell', sell_gold, name='sell_gold'),

    # Reporting
    path('reporting', reporting, name='reporting'),
    path('api/reports/filter/', filter_transactions_ajax, name='filter_transactions_ajax'),
    path('api/reports/export/', export_transactions_excel, name='export_transactions_excel'),

    # Backup
    path('backup/', backup, name='backup'),
    path('backup/create/', create_backup, name='create_backup'),
]