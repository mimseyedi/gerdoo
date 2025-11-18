import json
import jdatetime
from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from datetime import timedelta, datetime, date
from django.db.models import Sum, DecimalField
from django.contrib.auth.decorators import login_required
from ..models import (
    Transaction,
    Card,
    Category,
    Gold,
)
from ..utils import (
    get_jalali_date,
    format_currency,
    MONTHS_NAME,
    convert_sut_to_gram,
)


def get_most_expensive_category():
    cyear = datetime.now().year
    most_expensive = Transaction.objects.filter(
        kind='E',
        date__year=cyear,
    ).values('category').annotate(
        total_spent=Sum(
            'amount',
            output_field=DecimalField(),
        )
    ).order_by('-total_spent').first()

    if most_expensive:
        try:
            category_id = most_expensive['category']
            most_expensive_category = Category.objects.get(pk=category_id)
            most_expensive_category.total_spent = most_expensive['total_spent']
            return most_expensive_category
        except Category.DoesNotExist:
            return None
    return None


def get_least_expensive_category():
    cyear = datetime.now().year
    least_expensive = Transaction.objects.filter(
        kind='E',
        date__year=cyear,
    ).values('category').annotate(
        total_spent=Sum(
            'amount',
            output_field=DecimalField(),
        )
    ).order_by('total_spent').first()

    if least_expensive:
        try:
            category_id = least_expensive['category']
            least_expensive_category = Category.objects.get(pk=category_id)
            least_expensive_category.total_spent = least_expensive['total_spent']
            return least_expensive_category
        except Category.DoesNotExist:
            return None
    return None


def get_current_month_transactions(kind='E'):
    jtoday = jdatetime.date.today()
    jyear, jmonth = jtoday.year, jtoday.month

    j_start_date = jdatetime.date(
        jyear,
        jmonth,
        1,
    )

    if jmonth < 12:
        j_next_month = jdatetime.date(
            jyear,
            jmonth + 1,
            1,
        )
    else:
        j_next_month = jdatetime.date(
            jyear + 1,
            1,
            1,
        )

    g_start_date = j_start_date.togregorian()
    g_end_date = j_next_month.togregorian() - timedelta(days=1)

    days_passed = (jdatetime.date.today() - j_start_date).days + 1

    transactions = Transaction.objects.filter(
        kind=kind,
        date__range=[g_start_date, g_end_date],
    ).order_by('-date')

    total_amount = transactions.aggregate(
        total=Sum('amount')
    )['total'] or Decimal(0)

    cat_summary = transactions.values(
        'category__name',
        'category__id',
    ).annotate(
        amount=Sum('amount')
    ).order_by('-amount')

    final_cat = {}
    total_amount_for_division = total_amount or Decimal(1)

    for item in cat_summary:
        category_name = item['category__name']
        category_id = item['category__id']
        amount = item['amount']

        percentage = round(
            (amount / total_amount_for_division) * 100,
            2,
        )
        final_cat[category_name] = [
            format_currency(amount),
            percentage,
            category_id,
        ]

    return {
        'transactions': transactions,
        'total_amount': total_amount,
        'categories_summary': final_cat,
        'days_passed': days_passed,
    }


@login_required
def monthly_data_api(request):
    kind = request.GET.get('kind', 'E')

    if kind not in ['E', 'I', 'T']:
        return JsonResponse(
            {
                'error': 'Invalid kind parameter',
            },
            status=400,
        )

    data = get_current_month_transactions(kind=kind)

    total_amount = data['total_amount']
    categories_summary = data['categories_summary']
    days_passed = data['days_passed']

    if days_passed > 0 and total_amount > 0:
        average_daily = total_amount / days_passed
    else:
        average_daily = Decimal(0)

    return JsonResponse({
        'total_amount': format_currency(total_amount),
        'categories_summary': categories_summary,
        'average_daily': format_currency(average_daily),
        'kind': kind,
    })


def get_yearly_summary_data(kind: str, year=None) -> list:
    current_jdate = jdatetime.date.today()
    j_year = current_jdate.year if year is None else year

    start_jdate = jdatetime.date(
        j_year,
        1,
        1,
    )
    start_gdate = start_jdate.togregorian()

    if j_year == current_jdate.year:
        end_gdate = current_jdate.togregorian()
    else:
        end_jdate = jdatetime.date(
            j_year,
            12,
            29,
        )
        end_gdate = end_jdate.togregorian()

    yearly_transactions = Transaction.objects.filter(
        kind=kind,
        date__gte=start_gdate,
        date__lte=end_gdate,
    ).values('date', 'amount')

    yearly_summary = {}

    for transaction in yearly_transactions:
        g_date = transaction['date']
        j_date = jdatetime.date.fromgregorian(date=g_date)

        if j_date.year == j_year:
            j_month_index = j_date.month
            amount = float(transaction['amount'] or 0)

            if j_month_index in yearly_summary:
                yearly_summary[j_month_index]['total_amount'] += amount
            else:
                month_name = MONTHS_NAME[j_month_index - 1].strip()
                yearly_summary[j_month_index] = {
                    'month_name_fa': month_name,
                    'total_amount': amount,
                }

    final_list = []
    for m in range(1, 13):
        month_name = MONTHS_NAME[m - 1].strip()

        if m in yearly_summary:
            final_list.append(yearly_summary[m])
        else:
            final_list.append(
                {
                    'month_name_fa': month_name,
                    'total_amount': 0,
                }
            )
    return final_list


@login_required
def get_annual_chart_data(request):
    kind = request.GET.get('kind', 'E').upper()
    yearly_data = get_yearly_summary_data(kind=kind)

    chart_labels = [
        item['month_name_fa']
        for item in yearly_data
    ]

    chart_series = [
        item['total_amount']
        for item in yearly_data
    ]

    return JsonResponse({
        'labels': chart_labels,
        'series': chart_series,
    })


@login_required
def category_tag_report_api(request):
    category_id = request.GET.get('category_id')
    kind = request.GET.get('kind', 'E')

    if not category_id:
        return JsonResponse(
            {
                'error': 'Category ID is required.',
            },
            status=400,
        )

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse(
            {
                'error': 'Category not found.',
            },
            status=404,
        )

    jtoday = jdatetime.date.today()
    jyear, jmonth = jtoday.year, jtoday.month

    j_start_date = jdatetime.date(
        jyear,
        jmonth,
        1,
    )
    j_next_month = jdatetime.date(
        jyear,
        jmonth + 1,
        1,
    ) if jmonth < 12 else jdatetime.date(
        jyear + 1,
        1,
        1,
    )

    g_start_date = j_start_date.togregorian()
    g_end_date = j_next_month.togregorian()

    transactions_in_category = Transaction.objects.filter(
        kind=kind,
        category=category,
        date__gte=g_start_date,
        date__lt=g_end_date,
    )

    total_category_amount = transactions_in_category.aggregate(
        total=Sum('amount')
    )['total'] or Decimal(0)

    if total_category_amount == Decimal(0):
        return JsonResponse({
            'category_name': category.name,
            'total_category_amount_formatted': format_currency(Decimal(0)),
            'total_tagged_amount_formatted': format_currency(Decimal(0)),
            'tags_summary': [],
        })

    tagged_transactions_amount = Transaction.objects.filter(
        tags__isnull=False
    ).aggregate(
        total=Sum('amount')
    )['total'] or Decimal(0)

    tagged_transactions_qs = transactions_in_category.filter(
        tags__isnull=False
    ).distinct()

    tagged_transactions_amount = tagged_transactions_qs.aggregate(
        total=Sum('amount')
    )['total'] or Decimal(0)

    amount_untagged = total_category_amount - tagged_transactions_amount

    tag_summary = transactions_in_category.values(
        'tags__name'
    ).annotate(
        amount=Sum(
            'amount',
            distinct=True,
        )
    ).filter(
        tags__name__isnull=False
    ).order_by('-amount')

    final_tags = []

    for item in tag_summary:
        tag_name = item['tags__name']
        amount = item['amount']

        percentage = round((amount / total_category_amount) * 100, 2)

        final_tags.append(
            {
                'tag_name': tag_name,
                'amount_raw': amount,
                'amount_formatted': format_currency(amount),
                'percentage': percentage,
                'is_untagged': False,
            }
        )

    if amount_untagged > Decimal(0):
        untagged_percentage = round(
            (amount_untagged / total_category_amount) * 100,
            2,
        )

        final_tags.append(
            {
                'tag_name': 'بدون تگ',
                'amount_raw': amount_untagged,
                'amount_formatted': format_currency(amount_untagged),
                'percentage': untagged_percentage,
                'is_untagged': True,
            }
        )

    final_tags.sort(
        key=lambda x: x['amount_raw'],
        reverse=True,
    )

    return JsonResponse(
        {
            'category_name': category.name,
            'total_category_amount_formatted': format_currency(total_category_amount),
            'total_tagged_amount_formatted': format_currency(tagged_transactions_amount),
            'tags_summary': final_tags,
        }
    )


@login_required
def dashboard(request):
    current_date = date.today()
    jy, jm, _ = get_jalali_date(current_date).split('/')

    cards = Card.objects.filter(active=True)
    golds = Gold.objects.filter(is_sold=False)
    all_golds = Gold.objects.all()
    sold_golds = Gold.objects.filter(is_sold=True)

    total_gold = 0
    for g in golds:
        total_gold += g.weight

    total_gold_price = 0
    total_all_gold = 0
    for g in all_golds:
        total_gold_price += g.price
        total_all_gold += g.weight

    f_total_all_gold = convert_sut_to_gram(total_all_gold)
    total_all_gold_label = 'سوت'

    if f_total_all_gold < 1:
        total_all_gold = f'{total_all_gold:,.0f}'
    else:
        total_all_gold = f_total_all_gold
        total_all_gold_label = 'گرم'

    f_total_gold = convert_sut_to_gram(total_gold)
    total_gold_label = 'سوت'

    if f_total_gold < 1:
        total_gold = f'{total_gold:,.0f}'
    else:
        total_gold = f_total_gold
        total_gold_label = 'گرم'

    total_sold_gold = 0
    total_sold_price = 0
    for g in sold_golds:
        total_sold_gold += g.weight
        total_sold_price += g.p_price

    f_total_sold_gold = convert_sut_to_gram(total_sold_gold)
    total_sold_gold_label = 'سوت'

    if f_total_sold_gold < 1:
        total_sold_gold = f'{total_sold_gold:,.0f}'
    else:
        total_sold_gold = f_total_sold_gold
        total_sold_gold_label = 'گرم'

    total_balance = 0
    for c in cards:
        total_balance += int(c.balance)

    monthly_data = get_current_month_transactions(kind='E')
    current_expenses = monthly_data['transactions']
    total_current_expenses = monthly_data['total_amount']
    final_e_cat = monthly_data['categories_summary']
    days_passed = monthly_data['days_passed']
    total_current_expenses_raw_str = str(total_current_expenses)

    yearly_expenses_data = get_yearly_summary_data(kind='E')

    chart_labels = [item['month_name_fa'] for item in yearly_expenses_data]
    chart_series = [item['total_amount'] for item in yearly_expenses_data]

    y_status = True
    for x in chart_series:
        if x > 0:
            break
    else:
        y_status = False

    top_e = get_most_expensive_category()
    low_e = get_least_expensive_category()

    context = {
        'cards': cards,
        'total_balance': format_currency(total_balance),
        'current_month': MONTHS_NAME[int(jm) - 1],
        'current_year': jy,
        'current_e': current_expenses,
        'total_current_e': format_currency(total_current_expenses),
        'e_cat': final_e_cat,
        'total_current_expenses_raw': total_current_expenses_raw_str,
        'days_passed': days_passed,
        'yearly_chart_labels': json.dumps(chart_labels),
        'yearly_chart_series': json.dumps(chart_series),
        'year_status': y_status,
        'total_gold': total_gold,
        'total_gold_label': total_gold_label,
        'total_gold_price': total_gold_price,
        'total_sold_gold': total_sold_gold,
        'total_sold_gold_label': total_sold_gold_label,
        'total_sold_price': total_sold_price,
        'total_all_gold': total_all_gold,
        'total_all_gold_label': total_all_gold_label,
        'top_e': top_e,
        'low_e': low_e,
    }

    return render(request, 'main/dashboard.html', context)