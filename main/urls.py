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
]