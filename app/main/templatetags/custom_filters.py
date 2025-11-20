from django import template
from decimal import Decimal
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
def format_currency(value):
    if value is None:
        return ""
    try:
        number = Decimal(value)
        integer_part = int(number)
        return "{:,}".format(integer_part)
    except Exception: return value


@register.filter
@stringfilter
def format_persian_numbers(value):
    PERSIAN_NUMBERS = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
        '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹',
    }
    text = str(value)
    for eng, per in PERSIAN_NUMBERS.items():
        text = text.replace(eng, per)
    return mark_safe(text)


@register.filter
def jalali_date(value):
    def get_jalali_date(date):
        from jdatetime import datetime as jdt
        if date is None:
            return ""
        return jdt.fromgregorian(datetime=date).strftime('%Y/%m/%d')
    return get_jalali_date(value)


@register.filter
def times(value, arg):
    try:
        return Decimal(value) * Decimal(arg)
    except (ValueError, TypeError):
        return value


@register.filter
def format_card_number(number):
    first = number[:4]
    last = number[-4:]
    return f"{last} **** **** {first}"


@register.filter
def format_card_number_last4(number):
    last = number[-4:]
    return last


@register.filter
def format_card_number_with_space(number):
    p1 = number[-4:]
    p2 = number[-8:-4]
    p3 = number[4:8]
    p4 = number[:4]
    return f"{p1} {p2} {p3} {p4}"