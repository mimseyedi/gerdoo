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


urlpatterns = [
    # Home
    path('', home, name="home"),

    # Authenticating
    path('login', login_view, name="login"),
    path('logout', logout_view, name='logout'),
]