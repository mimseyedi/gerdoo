from django.shortcuts import (
    render,
    redirect,
)
from django.contrib.auth import (
    login,
    logout,
    authenticate,
)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            context = {
                'login_error': 'نام کاربری یا رمز عبور وارد شده صحیح نیست.'
            }
            return render(request, 'main/auth.html', context)

    return render(request, 'main/auth.html')


def logout_view(request):
    logout(request)
    return redirect('login')