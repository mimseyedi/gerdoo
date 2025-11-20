import uuid
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from .utils import (
    get_jalali_date,
    BANK_CHOICES,
    CARD_COLOR_CHOICES,
    TRANSACTION_AND_KIND_CHOICES,
)


class Card(models.Model):
    name = models.CharField(
        max_length=100,
        choices=BANK_CHOICES,
        verbose_name="نام بانک",
    )
    owner = models.CharField(
        max_length=100,
        verbose_name="نام صاحب حساب",
    )
    number = models.CharField(
        max_length=100,
        verbose_name="شماره کارت",
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        default=0,
        verbose_name="موجودی",
    )
    color = models.CharField(
        max_length=7,
        choices=CARD_COLOR_CHOICES,
        default='#007bff',
        verbose_name="رنگ کارت",
    )
    active = models.BooleanField(
        default=True,
        verbose_name='فعال',
    )

    class Meta:
        verbose_name = "کارت"
        verbose_name_plural = "کارت‌ها"

    def __str__(self):
        return f"{self.name} - {self.owner} - {self.number}"


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="نام دسته بندی",
    )
    kind = models.CharField(
        max_length=1,
        choices=TRANSACTION_AND_KIND_CHOICES,
        default='E',
        verbose_name='نوع دسته بندی',
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="نام تگ",
    )

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"

    def __str__(self):
        return self.name


class Transaction(models.Model):
    kind = models.CharField(
        max_length=1,
        choices=TRANSACTION_AND_KIND_CHOICES,
        verbose_name="نوع تراکنش",
    )
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        validators=[MinValueValidator(0)],
        verbose_name="مبلغ (ریال)",
    )
    source = models.ForeignKey(
        Card,
        on_delete=models.PROTECT,
        related_name='outgoing_transactions',
        null=True,
        blank=True,
        verbose_name="حساب مبدا",
    )
    source_balance_after = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="موجودی حساب مبدا پس از تراکنش",
    )
    destination = models.ForeignKey(
        Card,
        on_delete=models.PROTECT,
        related_name='incoming_transactions',
        null=True,
        blank=True,
        verbose_name="حساب مقصد",
    )
    destination_balance_after = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        null=True,
        blank=True,
        verbose_name="موجودی حساب مقصد پس از تراکنش",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name="دسته‌بندی",
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="تاریخ تراکنش",
    )
    description = models.TextField(
        blank=False,
        verbose_name="توضیحات",
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        verbose_name="تگ‌ها",
    )

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"
        ordering = ['-date']

    def __str__(self):
        jalali_dt = get_jalali_date(self.date)
        return f"{self.get_kind_display()} - {self.amount:,} تومان در تاریخ {jalali_dt}"


class Gold(models.Model):
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=Decimal(0),
        verbose_name='وزن طلا (سوت)',
    )
    price = models.DecimalField(
        max_digits=30,
        decimal_places=0,
        default=Decimal(0),
        verbose_name='مبلغ خرید (ریال)',
    )
    p_price = models.DecimalField(
        max_digits=30,
        decimal_places=0,
        default=Decimal(0),
        null=True,
        blank=True,
        verbose_name='مبلغ فروش (ریال)',
    )
    date = models.DateTimeField(
        default=timezone.now,
        verbose_name='تاریخ خرید',
    )
    p_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ فروش',
    )
    is_sold = models.BooleanField(
        default=False,
        verbose_name='فروخته شده',
    )
    description = models.TextField(
        blank=True,
        verbose_name='توضیحات',
    )

    class Meta:
        verbose_name = 'طلا'
        verbose_name_plural = 'طلاها'
        ordering = ['-date']

    @property
    def profit(self):
        if self.is_sold and self.p_price is not None:
            price_buy = self.price if self.price is not None else Decimal(0)
            price_sell = self.p_price
            profit_amount = price_sell - price_buy
            return profit_amount
        return None

    @property
    def profit_percentage(self):
        if self.profit is not None and self.price is not None and self.price > Decimal(0):
            percentage = (self.profit / self.price) * 100
            return round(percentage, 2)
        return None

    def __str__(self):
            jalali_dt = get_jalali_date(self.date)
            status = "فروخته شده" if self.is_sold else "موجود"
            return f"{self.weight} سوت طلا در تاریخ {jalali_dt} | {status}"


class BackupHistory(models.Model):
    uid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="شناسه",
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="تاریخ پشتیبان‌گیری",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='توضیحات',
    )

    class Meta:
        verbose_name = "پشتیبان‌گیری"
        verbose_name_plural = "پشتیبان‌گیری‌ها"
        ordering = ['-date']

    def __str__(self):
        jalali_dt = get_jalali_date(self.date)
        return f"پشتیبان‌گیری در تاریخ {jalali_dt} با شناسه {self.uid} - {self.description}"

