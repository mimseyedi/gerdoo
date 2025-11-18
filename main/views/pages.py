from django.shortcuts import (
    render,
    redirect,
)


def custom_page_not_found(request, *args, **kwargs):
    return render(request, 'main/404.html', {}, status=404)


def access_denied_view(request):
    return render(request, 'main/no_auth.html', {})


def home(request):
    return redirect('login')