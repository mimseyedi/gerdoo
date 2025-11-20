from django.shortcuts import render


def guide(request):
    return render(request, 'main/guide.html', {})