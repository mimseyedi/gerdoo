import jdatetime
from datetime import date
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import (
    Q,
    Sum,
    Count,
)
from ..models import (
    Category,
    Transaction,
)
from ..utils import (
    MONTHS_NAME,
    get_jalali_date,
    get_date_range_persian,
    format_card_number_last4,
)


@login_required
def categories(request):
    current_date = date.today()
    jy, jm, _ = get_jalali_date(current_date).split('/')
    context = {
        'jy': jy,
        'jm': MONTHS_NAME[int(jm) - 1],
    }
    return render(request, 'main/categories.html', context)


@login_required
@require_http_methods(["GET"])
def get_filtered_categories_ajax(request):
    category_type = request.GET.get('type', 'all')
    time_filter = request.GET.get('time', 'month')

    start_date, end_date = get_date_range_persian(time_filter)

    amount_filters = Q(
        date__gte=start_date,
        date__lt=end_date,
    )
    if category_type != 'all':
        amount_filters &= Q(kind=category_type)

    total_amount_in_scope = Transaction.objects.filter(
        amount_filters
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    if total_amount_in_scope == 0:
        total_amount_in_scope = 1

    category_queryset = Category.objects.all()
    if category_type != 'all':
        category_queryset = category_queryset.filter(kind=category_type)

    annotation_filters = Q(
        transaction__date__gte=start_date,
        transaction__date__lt=end_date,
    )
    if category_type != 'all':
        annotation_filters &= Q(
            transaction__kind=category_type
        )

    categories_with_stats = category_queryset.annotate(
        total_amount=Sum(
            'transaction__amount',
            filter=annotation_filters,),
        transaction_count=Count(
            'transaction',
            filter=annotation_filters,),
    ).order_by(
        '-total_amount',
        'name',
    )

    color_map = {
        'E': 'danger',
        'I': 'success',
        'T': 'info',
    }

    final_list = []
    for category in categories_with_stats:
        amount = category.total_amount or 0
        transaction_count = category.transaction_count or 0

        percent = (amount / total_amount_in_scope) * 100 if amount > 0 else 0

        formatted_amount = f"{int(amount):,}"

        final_list.append({
            'id': category.id,
            'name': category.name,
            'type_code': category.kind,
            'type_display': category.get_kind_display(),
            'color': color_map.get(category.kind, 'secondary'),
            'percent': round(percent, 1),
            'total_amount': formatted_amount,
            'transaction_count': transaction_count,
        })

    return JsonResponse(
        {
            'categories': final_list,
            'status': 'success',
            'time_filter': time_filter,
        },
    )


@login_required
@require_http_methods(["POST"])
def add_category_ajax(request):
    try:
        name = request.POST.get('name')
        kind = request.POST.get('kind')

        if not name or not kind:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'نام و نوع دسته‌بندی الزامی است.',
                },
                status=400,
            )

        cats = Category.objects.all()
        for c in cats:
            if name == c.name and kind == c.kind:
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'این دسته بندی از قبل ثبت شده است!',
                    },
                    status=400,
                )
        else:
            Category.objects.create(
                name=name,
                kind=kind,
            )
            return JsonResponse(
                {
                    'status': 'success',
                    'message': f'دسته‌بندی "{name}" با موفقیت ثبت شد.',
                    'new_category_name': name,
                },
            )
    except Exception as e:
        return JsonResponse(
            {
                'status': 'error',
                'message': f'خطا در ثبت: {str(e)}',
            },
            status=500,
        )


@login_required
@require_http_methods(["GET"])
def get_category_transactions_ajax(request):
    category_id = request.GET.get('category_id')
    time_filter = request.GET.get('time_filter', 'month')

    if not category_id:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'شناسه دسته‌بندی الزامی است.',
            },
            status=400,
        )

    try:
        start_date, end_date = get_date_range_persian(time_filter)

        transactions = Transaction.objects.filter(
            category_id=category_id,
            date__gte=start_date,
            date__lt=end_date,
        ).select_related(
            'source', 'destination',
        ).order_by('-date')

        category_name = Category.objects.get(id=category_id).name

        transaction_list = []
        for t in transactions:
            jalali_date = jdatetime.datetime.fromgregorian(
                date=t.date
            ).strftime('%Y/%m/%d')

            source_display = "نامشخص"
            destination_display = "نامشخص"

            if t.source:
                if t.source.active:
                    source_display = (f"{t.source.get_name_display()} ({t.source.owner}) - "
                                      f"{format_card_number_last4(t.source.number)}")
                else:
                    source_display = (f"{t.source.get_name_display()} ({t.source.owner}) - "
                                      f"{format_card_number_last4(t.source.number)} - غیرفعال")

            if t.destination:
                if t.destination.active:
                    destination_display = (f"{t.destination.get_name_display()} ({t.destination.owner}) - "
                                           f"{format_card_number_last4(t.destination.number)}")
                else:
                    destination_display = (f"{t.destination.get_name_display()} ({t.destination.owner}) - "
                                           f"{format_card_number_last4(t.destination.number)} - غیرفعال")

            transaction_list.append(
                {
                    'kind_display': t.get_kind_display(),
                    'amount': f"{int(t.amount):,}",
                    'date': jalali_date,
                    'source_display': source_display,
                    'destination_display': destination_display,
                    'description': t.description,
                    'kind_code': t.kind,
                },
            )
        return JsonResponse(
            {
                'status': 'success',
                'transactions': transaction_list,
                'category_name': category_name,
            },
        )
    except Category.DoesNotExist:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'دسته‌بندی یافت نشد.',
            },
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {
                'status': 'error',
                'message': f'خطا در بارگذاری تراکنش‌ها: {str(e)}',
            },
            status=500,
        )