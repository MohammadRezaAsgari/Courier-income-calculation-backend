from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import transaction
from datetime import timedelta
from .models import *

@receiver(post_save, sender=Travel)
@receiver(post_save, sender=Bonus)
@receiver(post_save, sender=Penalty)
def create_or_update_daily_income(sender, instance, **kwargs):
    '''
        based on the sender,we should create a new daily object or modify the existing one.
    '''
    if sender == Penalty:
        income_value = -(instance.value)
    else:
        income_value = instance.value

    with transaction.atomic():
        daily_income, created = DailyIncome.objects.get_or_create(
            courier = instance.courier,
            date = instance.date
        )

        '''
            if the daily exists, so we need to remove the impact of it from related weekly object.
            because if we dont do this, based on the weekly signal that is called post_save of the daily,
            it adds the whole new income of daily to related weekly object.
            we should remove the impact of old daily from weekly.
            so when we save this daily, that signal runs and the weekly object gets true income.
        '''
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
    '''
        based on the daily object that is created or modified,we should create a new weekly object or modify the existing one.
    '''
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


@receiver(pre_save, sender=Travel)
@receiver(pre_save, sender=Bonus)
@receiver(pre_save, sender=Penalty)
def pre_save_update_daily_and_weekly(sender, instance, **kwargs):
    '''
        handling update on Travels, Bonuses or Penalties.
        If these objects after creation are being modified, so if we dont use this signal, 
        the whole new value(income) is going to be added to the daily and weekly incomes onjects!
        
        this signal runs before updating Travels, Bonuses or Penalties, and remove the impact of them on target daily and weekly objects
        and when post_save signal runs, the new values are added to the daily and weekly income objects.
    '''

    if instance.pk is None:
        '''
            if the sender is just created so this action is not an update, return
        '''
        return
    
    with transaction.atomic():
        '''
            disable weekly signal(that is runed post_save on daily), because if we remove the impact of Travels, Bonuses or Penalties on the target daily object
            and save it, this will run that signal and make the incomes wrong.
            after applying the modifications, we will enable it back.
        '''
        post_save.disconnect(create_or_update_weekly_income, sender=DailyIncome)

        '''
            get the old value of the sender before updating
        '''
        old_value = sender.objects.get(pk=instance.pk).value
        
        daily_income, created = DailyIncome.objects.get_or_create(
            courier = instance.courier,
            date = instance.date
        )

        '''
            if the daily is just created, dont run the modification.
            this would not happen but check it for confidence of the code
        '''
        if created:
            return
        
        '''
            if the sender is penalty object, we should remove the impact of a penalty on daily income.
            so we should add the old value.
            otherwise the impact should be subtracted.
        '''
        if sender == Penalty:
            daily_income.income += old_value
        else:
            daily_income.income -= old_value
        daily_income.save()  

        '''
            do the same on the target weekly object.
        '''
        date = calculate_last_saturday(instance.date)
        weekly_income, created = WeeklyIncome.objects.get_or_create(
            courier = instance.courier,
            saturday_date = date
        )

        if created:
            return
        
        if sender == Penalty:
            weekly_income.income += old_value
        else:
            weekly_income.income -= old_value
        weekly_income.save()   

        '''
            enabling the signal
        '''
        post_save.connect(create_or_update_weekly_income, sender=DailyIncome)


def calculate_last_saturday(date):
    '''
        returns the last saturday based on the date.
        if the weekday of the input date in 5, this is a saturday
        otherwise go back to the first day of the week(Monday)
        and go back another 2 days, that is the last Saturday
    ''' 
    date_weekday = date.weekday()
    if date_weekday != 5:
        date = date - timedelta(days=date_weekday) - timedelta(days=2)
    return date