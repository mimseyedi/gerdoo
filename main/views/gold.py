from decimal import Decimal
from django.utils import timezone
from django.db import transaction
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from ..models import (
    Gold,
    Card,
    Category,
    Transaction,
)


@login_required
def gold(request):
    golds = Gold.objects.all()
    cards = Card.objects.filter(active=True)
    context = {
        'golds': golds,
        'cards': cards,
    }
    return render(request, 'main/gold.html', context)


@login_required
@require_POST
def add_gold(request):
    CATEGORY_NAME_FOR_PURCHASE = 'سرمایه گذاری'

    try:
        with transaction.atomic():
            action_type = request.POST.get('action_type')
            is_buying = (action_type == 'buy')

            source_card_id = request.POST.get('source_card')
            description = request.POST.get('description', '')

            weight_str = request.POST.get('weight', '').replace(',', '').replace('،', '')
            price_str = request.POST.get('price', '').replace(',', '').replace('،', '')

            if not is_buying: price_str = '0'

            try:
                weight, price = Decimal(weight_str), Decimal(price_str)
            except Exception:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'وزن یا مبلغ خرید نامعتبر است.',
                    },
                    status=400,
                )
            if weight < 0 or price < 0:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'وزن و مبلغ خرید باید مثبت باشند.',
                    },
                    status=400,
                )

            source_card = None
            if is_buying:
                if not source_card_id:
                    return JsonResponse(
                        {
                            'success': False,
                            'message': 'در حالت خرید، حساب مبدأ الزامی است.',
                        },
                        status=400,
                    )
                try:
                    source_card = Card.objects.select_for_update().get(id=source_card_id)
                except Card.DoesNotExist:
                    return JsonResponse(
                        {
                            'success': False,
                            'message': 'حساب مبدأ نامعتبر است.',
                        },
                        status=400,
                    )

                transaction_category, _ = Category.objects.get_or_create(
                    name=CATEGORY_NAME_FOR_PURCHASE,
                    defaults={'kind': 'E',},
                )

                current_balance = Decimal(source_card.balance)
                if price > current_balance:
                    return JsonResponse(
                        {
                            'success': False,
                            'message': f'موجودی حساب ({current_balance:,}'
                                       f' تومان) برای این خرید کافی نیست.',
                        },
                        status=400,
                    )
                source_card.balance = current_balance - price
                source_card.save()

            Gold.objects.create(
                weight=weight,
                price=price,
                date=timezone.now(),
                description=description,
            )

            if is_buying and price != 0:
                Transaction.objects.create(
                    kind='E',
                    amount=price,
                    date=timezone.now(),
                    source=source_card,
                    destination=None,
                    category=transaction_category,
                    description=f'خرید {weight} سوت طلا',
                )

            if is_buying:
                message = 'خرید طلا با موفقیت ثبت شد و مبلغ از حساب کسر گردید.'
            else:
                message = 'دریافت طلا (هدیه) با موفقیت ثبت شد.'

            return JsonResponse(
                {
                    'success': True,
                    'message': message,
                },
            )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'message': f'خطای سیستمی در ثبت خرید: {str(e)}',
            },
            status=500,
        )


@login_required
@require_POST
def sell_gold(request):
    CATEGORY_NAME_FOR_SALE = 'فروش دارایی'

    try:
        with transaction.atomic():
            gold_id = request.POST.get('gold_id')
            destination_card_id = request.POST.get('destination_card')
            selling_price_str = request.POST.get('selling_price', '').replace(',', '').replace('،', '')

            try:
                selling_price = Decimal(selling_price_str)
            except Exception:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'مبلغ فروش نامعتبر است.',
                    },
                    status=400,
                )
            if selling_price <= 0:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'مبلغ فروش باید یک عدد مثبت باشد.',
                    },
                    status=400,
                )
            try:
                gold_record = Gold.objects.select_for_update().get(id=gold_id)
            except Gold.DoesNotExist:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'رکورد طلا نامعتبر است.',
                    },
                    status=400,
                )

            try:
                destination_card = Card.objects.select_for_update().get(
                    id=destination_card_id
                )
            except Card.DoesNotExist:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'حساب مقصد نامعتبر است.',
                    },
                    status=400,
                )

            transaction_category, _ = Category.objects.get_or_create(
                name=CATEGORY_NAME_FOR_SALE,
                defaults={'kind': 'I', },
            )

            if gold_record.is_sold:
                return JsonResponse(
                    {
                        'success': False,
                        'message': 'این رکورد قبلاً فروخته شده است.',
                    },
                    status=400,
                )
            gold_record.is_sold = True
            gold_record.p_date = timezone.now()
            gold_record.p_price = selling_price
            gold_record.save()

            destination_card.balance = Decimal(destination_card.balance) + selling_price
            destination_card.save()

            Transaction.objects.create(
                kind='I',
                amount=selling_price,
                date=timezone.now(),
                source=None,
                destination=destination_card,
                category=transaction_category,
                description=f'فروش {gold_record.weight:,.0f} سوت طلا ',
            )

            return JsonResponse(
                {
                    'success': True,
                    'message': 'فروش با موفقیت ثبت شد و مبلغ به حساب واریز گردید.',
                },
            )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'message': f'خطای سیستمی در ثبت فروش: {str(e)}',
            },
            status=500,
        )