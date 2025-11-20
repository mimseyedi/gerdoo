from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import (
    Decimal,
    InvalidOperation,
)
from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.views.decorators.http import (
    require_POST,
    require_http_methods,
)
from ..models import Card
from ..utils import (
    BANK_CHOICES,
    CARD_COLOR_CHOICES,
    english_to_persian_numbers,
)


@login_required
def cards(request):
    status = request.GET.get('status', 'active')
    if status == 'active':
        cards_q = Card.objects.filter(active=True)
        status = 'active'
    else:
        cards_q = Card.objects.filter(active=False)

    context = {
        'cards': cards_q,
        'banks': BANK_CHOICES,
        'colors': CARD_COLOR_CHOICES,
        'status': status,
    }
    return render(request, 'main/cards.html', context)


@login_required
@require_http_methods(["POST"])
def add_card(request):
    name = request.POST.get('name', '').strip()
    owner = request.POST.get('owner', '').strip()
    number_raw = request.POST.get('number', '').strip()
    balance_raw = request.POST.get('balance', '0').strip()
    color = request.POST.get('color', '').strip()

    errors = {}

    if not name or name == '':
        errors['name'] = ["انتخاب نام بانک الزامی است."]
    if not owner:
        errors['owner'] = ["وارد کردن نام صاحب حساب الزامی است."]
    if not color:
        errors['color'] = ["انتخاب رنگ کارت الزامی است."]

    number = english_to_persian_numbers(number_raw)
    number = number.replace('-', '').replace(' ', '')

    if not number_raw:
        errors['name'] = ["وارد کردن شماره کارت الزامی است."]
    else:
        if len(number) != 16 or not number.isdigit():
            errors['number'] = ["شماره کارت باید دقیقاً ۱۶ رقم باشد."]

    balance_clean = balance_raw.replace(',', '')
    balance_value = 0
    try:
        balance_value = Decimal(balance_clean)
    except InvalidOperation:
        errors['balance'] = ["موجودی باید عدد باشد."]
    except ValueError:
        errors['balance'] = ["موجودی باید عدد باشد."]

    if not errors and balance_value < 0:
        errors['balance'] = ["موجودی اولیه نمی‌تواند منفی باشد."]

    if errors:
        return JsonResponse(
            {
                'success': False,
                'errors': errors,
            },
            status=400,
        )
    try:
        Card.objects.create(
            name=name,
            owner=owner,
            number=number,
            balance=balance_value,
            color=color,
        )
        return JsonResponse(
            {
                'success': True,
                'message': 'کارت جدید با موفقیت ثبت و ذخیره شد.',
            },
        )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'message': f'خطای داخلی در ذخیره‌سازی: {str(e)}',
            },
            status=500,
        )


@login_required
@require_POST
def activate_card(request):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(
            {
                'success': False,
                'message': 'درخواست نامعتبر است.',
            },
            status=400,
        )

    card_id = request.POST.get('card_id')

    if not card_id:
        return JsonResponse(
            {
                'success': False,
                'message': 'شناسه کارت ارسال نشده است.',
            },
            status=400,
        )
    try:
        card = get_object_or_404(Card, id=card_id)

        if card.active:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'کارت از قبل فعال است.',
                },
                status=400,
            )
        card.active = True
        card.save()

        return JsonResponse(
            {
                'success': True,
                'message': 'کارت با موفقیت فعال شد.',
            },
        )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'message': f'خطایی رخ داد: {str(e)}',
            },
            status=500,
        )


@login_required
@require_http_methods(["POST"])
def deactivate_card(request):
    card_id = request.POST.get('card_id')

    if not card_id:
        return JsonResponse(
            {
                'success': False,
                'message': 'شناسه کارت یافت نشد.',
            },
            status=400,
        )

    try:
        card = get_object_or_404(Card, id=card_id)

        card.active = False
        card.save()

        return JsonResponse(
            {
                'success': True,
                'message': 'کارت با موفقیت حذف/غیرفعال شد.',
            },
        )
    except Card.DoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'message': 'کارت مورد نظر یافت نشد.',
            },
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'message': str(e),
            },
            status=500,
        )