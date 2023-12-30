from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from datetime import timedelta
from .models import *

@receiver(post_save, sender=Travel)
@receiver(post_save, sender=Bonus)
@receiver(post_save, sender=Penalty)
def create_or_update_daily_income(sender, instance, **kwargs):
    if sender == Penalty:
        income_value = -(instance.value)
    else:
        income_value = instance.value

    with transaction.atomic():
        daily_income, created = DailyIncome.objects.get_or_create(
            courier = instance.courier,
            date = instance.date
        )

        if not created:
            date = instance.date
            date = calculate_last_saturday(date)
            the_week_object = WeeklyIncome.objects.get(courier = instance.courier, saturday_date = date)

            the_week_object.income -= daily_income.income
            the_week_object.save()

        daily_income.income += income_value
        daily_income.save()

@receiver(post_save, sender=DailyIncome)
def create_or_update_weekly_income(sender, instance, **kwargs):
    date = instance.date
    income_value = instance.income

    date = calculate_last_saturday(date)

    with transaction.atomic():
        weekly_income, _ = WeeklyIncome.objects.get_or_create(
            courier = instance.courier,
            saturday_date = date
        )
        
        weekly_income.income += income_value
        weekly_income.save()


def calculate_last_saturday(date):
    date_weekday = date.weekday()
    if date_weekday != 5:
        date = date - timedelta(days=date_weekday) - timedelta(days=2)
    return date