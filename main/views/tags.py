from django.db.models import Count
from django.shortcuts import render
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from ..models import Tag


@login_required
def tags(request):
    all_tags = Tag.objects.annotate(
        transaction_count=Count('transaction')
    ).order_by(
        '-transaction_count',
        '-id',
    )
    context = {
        'tags': all_tags,
        'total': all_tags.count(),
    }
    return render(request, 'main/tags.html', context)


@login_required()
def get_all_tags(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            tags = Tag.objects.values(
                'id',
                'name',
            ).order_by('name')

            tag_list = [
                {
                    'id': tag['id'],
                    'name': tag['name'],
                }
                for tag in tags
            ]
            return JsonResponse(
                {
                    'tags': tag_list,
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


@login_required
@require_POST
def add_tag_ajax(request):
    tag_name = request.POST.get('name', '').strip()

    if not tag_name:
        return JsonResponse(
            {
                'success': False,
                'errors': {
                    'name': 'نام تگ نمی‌تواند خالی باشد!',
                },
            },
            status=400,
        )

    try:
        Tag.objects.create(name=tag_name)
        return JsonResponse(
            {
                'success': True,
                'message': 'تگ با موفقیت اضافه شد.',
            },
        )
    except IntegrityError:
        return JsonResponse(
            {
                'success': False,
                'errors': {
                    'name': 'این تگ قبلاً در سیستم وجود دارد.',
                },
            },
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'errors': str(e),
            },
            status=500,
        )


@login_required
@require_POST
def delete_tag_ajax(request):
    tag_id = request.POST.get('tag_id')

    try:
        tag = Tag.objects.get(id=tag_id)
        tag.delete()
        return JsonResponse(
            {
                'success': True,
                'message': f'تگ "{tag.name}" با موفقیت حذف شد.',
            },
        )
    except Tag.DoesNotExist:
        return JsonResponse(
            {
                'success': False,
                'message': 'تگ مورد نظر یافت نشد.',
            },
            status=404,
        )
    except Exception as e:
        return JsonResponse(
            {
                'success': False,
                'message': f'خطا در حذف تگ: {e}',
            },
            status=500,
        )