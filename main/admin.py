from django.contrib import admin
from jalali_date.admin import ModelAdminJalaliMixin
from .utils import (
    format_currency,
    get_jalali_date,
)
from .models import (
    Card,
    Category,
    Transaction,
    Gold,
    BackupHistory,
    Tag,
)


@admin.register(Gold)
class GoldAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def formatted_amount(self, obj):
        return format_currency(obj.price) + " ریال"

    formatted_amount.short_description = "مبلغ خرید"
    formatted_amount.admin_order_field = 'amount'


    def formatted_p_amount(self, obj):
        return format_currency(obj.p_price) + " ریال"

    formatted_p_amount.short_description = "مبلغ فروش"
    formatted_p_amount.admin_order_field = 'p_amount'


    def jalali_date_display(self, obj):
        return get_jalali_date(obj.date) if obj.date else "-"

    jalali_date_display.short_description = "تاریخ خرید"
    jalali_date_display.admin_order_field = 'date'


    def jalali_p_date_display(self, obj):
        return get_jalali_date(obj.p_date) if obj.p_date else "-"

    jalali_p_date_display.short_description = "تاریخ فروش"
    jalali_p_date_display.admin_order_field = 'p_date'


    list_display = (
        'id',
        'weight',
        'formatted_amount',
        'formatted_p_amount',
        'jalali_date_display',
        'jalali_p_date_display',
        'description',
        'is_sold',
    )
    fields = (
        'weight',
        'price',
        'p_price',
        'date',
        'p_date',
        'is_sold',
        'description',
    )
    list_filter = ('is_sold',)
    search_fields = ('description',)
    date_hierarchy = 'date'


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    def formatted_balance(self, obj):
        return format_currency(obj.balance) + " ریال"

    formatted_balance.short_description = "موجودی"
    formatted_balance.admin_order_field = 'balance'


    list_display = (
        'id',
        'name',
        'owner',
        'number',
        'formatted_balance',
        'color',
        'active',
    )
    search_fields = (
        'name',
        'owner',
    )
    list_filter = (
        'owner',
        'active',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'kind',
    )
    fields = (
        'name',
        'kind',
    )
    list_filter = (
        'kind',
    )
    search_fields = (
        'name',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )
    fields = (
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(Transaction)
class TransactionAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def formatted_amount(self, obj):
        return format_currency(obj.amount) + " ریال"

    formatted_amount.short_description = "مبلغ"
    formatted_amount.admin_order_field = 'amount'


    def jalali_date_display(self, obj):
        return get_jalali_date(obj.date)   if obj.date else "-"

    jalali_date_display.short_description = "تاریخ تراکنش"
    jalali_date_display.admin_order_field = 'date'


    def formatted_source_balance_after(self, obj):
        if obj.source_balance_after is not None:
            return format_currency(obj.source_balance_after) + " ریال"

    formatted_source_balance_after.short_description = "موجودی حساب مبدا بعد از تراکنش"
    formatted_source_balance_after.admin_order_field = 'source_balance_after'


    def formatted_destination_balance_after(self, obj):
        if obj.destination_balance_after is not None:
            return format_currency(obj.destination_balance_after) + " ریال"

    formatted_destination_balance_after.short_description = "موجودی حساب مقصد بعد از تراکنش"
    formatted_destination_balance_after.admin_order_field = 'destination_balance_after'

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()[:3]])

    display_tags.short_description = 'تگ‌ها'


    list_display = (
        'id',
        'kind',
        'formatted_amount',
        'source',
        'formatted_source_balance_after',
        'destination',
        'formatted_destination_balance_after',
        'category',
        'jalali_date_display',
        'description',
        'display_tags',
    )
    fields = (
        'kind',
        'amount',
        'source',
        'source_balance_after',
        'destination',
        'destination_balance_after',
        'category',
        'description',
        'tags',
        'date',
    )
    list_filter = (
        'kind',
        'category',
    )
    filter_horizontal = (
        'tags',
    )
    search_fields = (
        'description',
    )
    date_hierarchy = 'date'


@admin.register(BackupHistory)
class BackupHistoryAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    def jalali_date_display(self, obj):
        return get_jalali_date(obj.date) if obj.date else "-"

    jalali_date_display.short_description = "تاریخ پشتیبان‌گیری"
    jalali_date_display.admin_order_field = 'date'


    list_display = (
        'id',
        'uid',
        'jalali_date_display',
        'description',
    )
    fields = (
        'date',
        'description',
    )
    search_fields = (
        'description',
    )
    date_hierarchy = 'date'