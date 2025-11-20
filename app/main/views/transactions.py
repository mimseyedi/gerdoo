import datetime
import jdatetime
from decimal import Decimal
from django.shortcuts import render
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from ..models import (
    Card,
    Category,
    Transaction,
)
from ..utils import (
    MONTHS_NAME,
    get_jalali_date,
    format_currency,
    get_month_year_list,
    format_card_number_last4,
    extract_commission_from_description,
)


@login_required
def get_transaction_details_by_id(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        transaction_id = request.GET.get('transaction_id')

        try:
            t = Transaction.objects.select_related(
                'source',
                'destination',
                'category',
            ).get(pk=transaction_id)

            source_name = "نامشخص"
            if t.source:
                source_name = (f"{t.source.get_name_display()} ({t.source.owner}) - "
                               f"{format_card_number_last4(t.source.number)}")
                if not t.source.active:
                    source_name += " - غیرفعال"

            destination_name = "نامشخص"
            if t.destination:
                destination_name = (f"{t.destination.get_name_display()} ({t.destination.owner}) - "
                                    f"{format_card_number_last4(t.destination.number)}")
                if not t.destination.active:
                    destination_name += " - غیرفعال"

            description = t.description
            if len(description) > 50:
                description = description[:50] + "..."

            data = {
                'id': t.id,
                'kind': t.get_kind_display(),
                'amount': format_currency(t.amount),
                'jalali_date': get_jalali_date(t.date),
                'category_name': t.category.name,
                'source_name': source_name,
                'destination_name': destination_name,
                'description': description,
            }

            return JsonResponse(
                {
                    'success': True,
                    'details': data,
                },
            )

        except Transaction.DoesNotExist:
            return JsonResponse(
                {
                    'success': False,
                    'errors': 'تراکنش مورد نظر یافت نشد.',
                },
                status=404,
            )
        except Exception as e:
            return JsonResponse(
                {
                    'success': False,
                    'errors': f'خطای سیستمی در بازیابی: {e}',
                },
                status=500,
            )

    return JsonResponse(
        {
            'success': False,
            'errors': 'درخواست نامعتبر.',
        },
        status=400,
    )


def get_transaction_details(transactions_queryset):
    transaction_data = []

    for t in transactions_queryset:
        source_card = None
        if t.source:
            if not t.source.active:
                source_card = (f"{t.source.get_name_display()} ({t.source.owner}) - "
                               f"{format_card_number_last4(t.source.number)} - غیرفعال")
            else:
                source_card = (f"{t.source.get_name_display()} ({t.source.owner}) - "
                               f"{format_card_number_last4(t.source.number)}")

        destination_card = None
        if t.destination:
            if not t.destination.active:
                destination_card = (f"{t.destination.get_name_display()} ({t.destination.owner}) - "
                                    f"{format_card_number_last4(t.destination.number)} - غیرفعال")
            else:
                destination_card = (f"{t.destination.get_name_display()} ({t.destination.owner}) - "
                                    f"{format_card_number_last4(t.destination.number)}")

        transaction_tags = [tag.name for tag in t.tags.all()]

        y, m, d = get_jalali_date(t.date).split('/')

        data = {
            'id': t.id,
            'kind': t.get_kind_display(),
            'amount_display': format_currency(t.amount),
            'source_card': source_card,
            'destination_card': destination_card,
            'category_name': t.category.name if t.category else None,
            'year': y,
            'month': MONTHS_NAME[int(m) - 1],
            'day': d,
            'tags': transaction_tags,
            'description': t.description,
            'source_balance_after': format_currency(
                t.source_balance_after) if t.source_balance_after is not None else None,
            'destination_balance_after': format_currency(
                t.destination_balance_after) if t.destination_balance_after is not None else None,
        }
        transaction_data.append(data)

    return transaction_data


@login_required
def transactions(request):
    current_year, current_month_index, months_list = get_month_year_list()

    today_jalali = get_jalali_date(timezone.now())

    first_day_greg = jdatetime.date(
        current_year,
        current_month_index,
        1,
    ).togregorian()

    if current_month_index == 12:
        next_month_greg = jdatetime.date(
            current_year + 1,
            1,
            1,
        ).togregorian()
    else:
        next_month_greg = jdatetime.date(
            current_year,
            current_month_index + 1,
            1,
        ).togregorian()

    last_day_greg = next_month_greg - datetime.timedelta(days=1)

    ta = Transaction.objects.filter(
        date__range=[
            first_day_greg,
            last_day_greg,
        ]
    ).order_by(
        '-date',
        '-id',
    )

    transaction_data = get_transaction_details(ta)

    tac = len(transaction_data)

    cards = Card.objects.filter(active=True)
    category = Category.objects.all()

    context = {
        'transactions': transaction_data,
        'today_jalali': today_jalali,
        'total': tac,
        'category': category,
        'cards': cards,
        'MONTHS_NAME': months_list,
        'current_year': current_year,
        'current_month_index': current_month_index,
    }

    return render(request, 'main/transactions.html', context)


@login_required
def get_transactions_by_month(request):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(
            {
                'error': 'درخواست نامعتبر.',
            },
            status=400,
        )

    try:
        month = request.GET.get('month')
        year = request.GET.get('year')

        if not month or not year:
            return JsonResponse(
                {
                    'error': 'ماه و سال الزامی است.',
                },
                status=400,
            )

        year, month = int(year), int(month)
        first_day_greg = jdatetime.date(
            year,
            month,
            1,
        ).togregorian()

        if month == 12:
            next_month_greg = jdatetime.date(
                year + 1,
                1,
                1,
            ).togregorian()
        else:
            next_month_greg = jdatetime.date(
                year,
                month + 1,
                1,
            ).togregorian()

        last_day_greg = next_month_greg - datetime.timedelta(days=1)

        ta = Transaction.objects.filter(
            date__range=[
                first_day_greg,
                last_day_greg,
            ]
        ).order_by(
            '-date',
            '-id',
        )
        transaction_data = get_transaction_details(ta)

        return JsonResponse(
            {
                'transactions': transaction_data,
                'total': len(transaction_data)
            },
        )
    except Exception as e:
        return JsonResponse(
            {
                'error': f'خطا در بازیابی داده: {e}',
            },
            status=500,
        )


@login_required
@require_POST
def add_transaction(request):
    try:
        with transaction.atomic():
            kind = request.POST.get('kind')
            amount_str = request.POST.get('amount').replace(',', '').replace('،', '')
            commission_str = request.POST.get('commission', '0').replace(',', '').replace('،', '')
            source_id = request.POST.get('source')
            destination_id = request.POST.get('destination')
            category_id = request.POST.get('category')
            transaction_date_jalali_str = request.POST.get('date')
            description = request.POST.get('description')
            tag_ids_str = request.POST.get('tags', '')

            errors = {}

            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    errors['amount'] = 'مبلغ باید یک عدد مثبت باشد!'
            except ValueError:
                errors['amount'] = 'وارد کردن مبلغ الزامی است!'

            commission = Decimal(0)
            if kind == 'T':
                if not commission_str or not commission_str.strip():
                    commission_str = '0'
                try:
                    commission = Decimal(commission_str)
                    if commission < 0:
                        errors['commission'] = 'کارمزد نمی‌تواند منفی باشد!'
                except ValueError:
                    errors['commission'] = 'کارمزد وارد شده نامعتبر است!'

            if kind not in ['I', 'E', 'T']:
                errors['kind'] = 'نوع تراکنش نامعتبر است!'

            source_card = None
            if kind in ['E', 'T'] and not source_id:
                errors['source'] = 'برای هزینه و انتقال، حساب مبدأ الزامی است!'

            if source_id and source_id.strip():
                try:
                    source_card = Card.objects.select_for_update().get(id=source_id)
                except Card.DoesNotExist:
                    errors['source'] = 'حساب مبدأ نامعتبر است!'

            destination_card = None
            if kind in ['I', 'T'] and not destination_id:
                errors['destination'] = 'برای درآمد و انتقال، حساب مقصد الزامی است!'

            if destination_id and destination_id.strip():
                try:
                    destination_card = Card.objects.get(id=destination_id)
                except Card.DoesNotExist:
                    errors['destination'] = 'حساب مقصد نامعتبر است!'

            if not category_id:
                errors['category'] = 'انتخاب دسته‌بندی تراکنش الزامی است!'
            else:
                try:
                    transaction_category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    errors['category'] = 'دسته‌بندی نامعتبر است!'

            if not transaction_date_jalali_str:
                return JsonResponse(
                    {
                        'success': False,
                        'errors': 'تاریخ تراکنش مورد نیاز است.',
                    },
                    status=400,
                )

            try:
                jalali_dt = jdatetime.datetime.strptime(
                    transaction_date_jalali_str,
                    '%Y/%m/%d',
                )
                transaction_date_gregorian = jalali_dt.togregorian().date()
            except ValueError:
                return JsonResponse(
                    {
                        'success': False,
                        'errors': 'قالب تاریخ ارسالی نامعتبر است. (انتظار: YYYY/MM/DD)',
                    },
                    status=400,
                )

            if not description:
                errors['description'] = 'نوشتن توضیحات الزامی است! (هر چند کوتاه ...)'

            if errors:
                return JsonResponse(
                    {
                        'success': False,
                        'errors': errors,
                    },
                    status=400,
                )

            if kind in ['E', 'T'] and source_card:
                total_deduction = amount

                if kind == 'T':
                    total_deduction = amount + commission

                current_balance = Decimal(source_card.balance)

                if total_deduction > current_balance:
                    errors['amount'] = f'موجودی حساب مبدا کافی نیست! (مبلغ {amount} + کارمزد {commission})'
                    return JsonResponse(
                        {
                            'success': False,
                            'errors': errors,
                        },
                        status=400,
                    )

                source_card.balance = current_balance - total_deduction
                source_card.save()
                source_balance_after = source_card.balance
            else:
                source_balance_after = None

            if kind in ['I', 'T'] and destination_card:
                current_balance = Decimal(destination_card.balance)

                destination_card.balance = current_balance + amount
                destination_card.save()
                destination_balance_after = destination_card.balance
            else:
                destination_balance_after = None

            if kind == 'T':
                description += f" (کارمزد: {commission} ریال)"

            new_transaction = Transaction.objects.create(
                kind=kind,
                amount=amount,
                date=transaction_date_gregorian,
                source=source_card if kind in ['E', 'T'] else None,
                source_balance_after=source_balance_after,
                destination=destination_card if kind in ['I', 'T'] else None,
                destination_balance_after=destination_balance_after,
                category=transaction_category,
                description=description,
            )

            if tag_ids_str:
                tag_ids = [
                    int(tag_id.strip())
                    for tag_id in tag_ids_str.split(',')
                    if tag_id.strip().isdigit()
                ]
                if tag_ids:
                    new_transaction.tags.set(tag_ids)

            return JsonResponse(
                {
                    'success': True,
                    'message': 'Transaction recorded successfully.',
                },
            )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'errors': str(e),
            },
            status=500,
        )


@require_POST
@login_required
def delete_transaction(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'درخواست نامعتبر.'}, status=400)

    transaction_id = request.POST.get('transaction_id')

    try:
        with transaction.atomic():
            t = Transaction.objects.select_for_update().get(pk=transaction_id)
            commission = extract_commission_from_description(t.description)
            kind, amount = t.kind, t.amount

            match kind:
                case 'E':
                    if t.source:
                        t.source.balance += amount
                        t.source.save()
                case 'I':
                    if t.destination:
                        t.destination.balance -= amount
                        t.destination.save()
                case 'T':
                    if t.source:
                        t.source.balance += amount
                        t.source.balance += commission
                        t.source.save()
                    if t.destination:
                        t.destination.balance -= amount
                        t.destination.save()
            t.delete()

            return JsonResponse(
                {
                    'success': True,
                    'message': 'تراکنش با موفقیت حذف شد و موجودی‌ها به‌روز شدند.',
                },
            )
    except Transaction.DoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'errors': 'تراکنش مورد نظر یافت نشد.',
            },
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'errors': f'خطای سیستمی در حذف تراکنش: {e}',
            },
            status=500,
        )


def get_categories_by_kind(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        kind = request.GET.get('kind')

        try:
            categories = Category.objects.filter(
                kind=kind
            ).order_by('name')

            category_list = [
                {
                    'id': cat.id,
                    'name': cat.name,
                }
                for cat in categories
            ]

            return JsonResponse(
                {
                    'categories': category_list,
                },
            )
        except Exception as e:
            return JsonResponse(
                {
                    'error': f'خطا در بازیابی داده: {e}',
                },
                status=500,
            )
    return JsonResponse(
        {
            'error': 'درخواست نامعتبر.',
        },
        status=400,
    )