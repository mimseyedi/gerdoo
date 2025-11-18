import re
import jdatetime
from datetime import timedelta, date
from decimal import Decimal, ROUND_HALF_UP


# CONSTs:

SUT_PER_GRAM = Decimal('1000')

TRANSACTION_AND_KIND_CHOICES = (
    ('I', 'درآمد'),
    ('E', 'هزینه'),
    ('T', 'انتقال'),
)

MONTHS_NAME = [
    'فروردین',
    'اردیبهشت',
    'خرداد',
    'تیر',
    'مرداد',
    'شهریور',
    'مهر',
    'آبان',
    'آذر',
    'دی',
    'بهمن',
    'اسفند',
]

CARD_COLOR_CHOICES = (
    ('#007bff', 'آبی',),
    ('#dc3545', 'قرمز',),
    ('#28a745', 'سبز',),
    ('#ffc107', 'زرد',),
    ('#6f42c1', 'بنفش',),
    ('#708090', 'سربی',),
    ('#343a40', 'مشکی ',),
)

BANK_CHOICES = (
    ('melli', 'بانک ملی',),
    ('saderat', 'بانک صادرات',),
    ('sepah', 'بانک سپه',),
    ('tejarat', 'بانک تجارت',),
    ('mellat', 'بانک ملت',),
    ('pasargad', 'بانک پاسارگاد',),
    ('ayande', 'بانک آینده',),
    ('blu', 'بانک بلو',),
    ('refah', 'بانک رفاه',),
    ('eghtesad_novin', 'بانک اقتصاد نوین',),
    ('shahr', 'بانک شهر',),
    ('parsian', 'بانک پارسیان',),
    ('keshavarzi', 'بانک کشاورزی',),
    ('saman', 'بانک سامان',),
)


# Functions:

def format_currency(amount):
    if amount is None:
        return ""
    return f"{amount:,.0f}"


def get_jalali_date(date):
    if date is None:
        return ""
    return jdatetime.datetime.fromgregorian(
        datetime=date
    ).strftime('%Y/%m/%d')


def format_card_number_last4(number):
    last = number[-4:]
    return last


def english_to_persian_numbers(text):
    translation_table = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')
    return text.translate(translation_table)


def get_date_range_persian(time_filter):

    today_greg = date.today()
    today_jalali = jdatetime.date.fromgregorian(date=today_greg)

    start_jalali, end_jalali = None, None

    if time_filter == 'year':
        start_jalali = jdatetime.date(
            today_jalali.year,
            1,
            1,
        )
        try:
            end_jalali = jdatetime.date(
                today_jalali.year,
                12,
                30,
            )
        except ValueError:
            end_jalali = jdatetime.date(
                today_jalali.year,
                12,
                29,
            )

    else:
        start_jalali = jdatetime.date(
            today_jalali.year,
            today_jalali.month,
            1,
        )

        month = today_jalali.month

        if month <= 6:
            end_day = 31
        elif month <= 11:
            end_day = 30
        else:
            try:
                jdatetime.date(
                    today_jalali.year,
                    12,
                    30,
                )
                end_day = 30
            except ValueError:
                end_day = 29

        end_jalali = jdatetime.date(
            today_jalali.year,
            today_jalali.month,
            end_day,
        )

    start_date_greg = start_jalali.togregorian()
    end_date_greg = end_jalali.togregorian() + timedelta(days=1)

    return start_date_greg, end_date_greg


def convert_sut_to_gram(sut_weight, precision=3):
    try:
        sut_decimal = Decimal(sut_weight)

        if sut_decimal <= 0:
            return Decimal(0)

        gram_weight = sut_decimal / SUT_PER_GRAM

        rounding_format = '0.' + '0' * precision
        return gram_weight.quantize(Decimal(rounding_format), rounding=ROUND_HALF_UP)

    except Exception as e:
        print(f"Error converting sut to gram: {e}")
        return None


def get_month_year_list():
    today = jdatetime.date.today()
    current_year = today.year

    months_list = {}
    for i in range(1, 13):
        months_list[i] = MONTHS_NAME[i - 1]
        
    return current_year, today.month, months_list


def extract_commission_from_description(description):
    if not description:
        return Decimal(0)

    commission_pattern = re.compile(r'\(کارمزد:\s*([0-9,،\u06F0-\u06F9]+)\s*ریال\)')

    match = commission_pattern.search(description)

    if match:
        amount_str = match.group(1)

        persian_to_english = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
        english_amount_str = amount_str.translate(persian_to_english)

        return Decimal(english_amount_str.replace(',', '').replace('،', ''))

    return Decimal(0)