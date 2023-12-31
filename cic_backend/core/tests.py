from django.test import TestCase
from .models import Courier, Travel, Bonus, Penalty, DailyIncome, WeeklyIncome
from datetime import datetime

class DailyIncomeTestCase(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(first_name='courier1_first_name',last_name='courier1_last_name')
        self.date = datetime.strptime('2023-12-08', '%Y-%m-%d')

        Travel.objects.create(courier = self.courier, value=1000, date = self.date)

    def test_daily_income_with_travel(self):
        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.date)
        self.assertEqual(daily_instance.income, 1000)

        Travel.objects.create(courier = self.courier, value=500, date = self.date)
        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.date)        
        self.assertEqual(daily_instance.income, 1500)


    def test_daily_income_with_travel_bonus_penalty(self):
        bonus = Bonus.objects.create(courier = self.courier, value=500, date = self.date)

        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.date)
        self.assertEqual(daily_instance.income, 1500)

        bonus.value = 400
        bonus.save()
        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.date)
        self.assertEqual(daily_instance.income, 1400)

        penalty = Penalty.objects.create(courier = self.courier, value=100, date = self.date)

        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.date)
        self.assertEqual(daily_instance.income, 1300)

        penalty.value = 50
        penalty.save()
        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.date)
        self.assertEqual(daily_instance.income, 1350)

    def test_daily_income_table_rows(self):
        self.assertEqual(DailyIncome.objects.all().values().count(), 1) 

class WeeklyIncomeTestCase(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(first_name='courier1_first_name',last_name='courier1_last_name')

        self.date1 = datetime.strptime('2023-12-02', '%Y-%m-%d')# <-- the date weekday is saturday
        self.date2 = datetime.strptime('2023-12-05', '%Y-%m-%d')# <-- the last saturday is 2023-12-02

        self.date3 = datetime.strptime('2023-12-09', '%Y-%m-%d')# <-- the date weekday is saturday
        self.date4 = datetime.strptime('2023-12-13', '%Y-%m-%d')# <-- the last saturday is 2023-12-09
        

        Travel.objects.create(courier = self.courier, value=1000, date = self.date1)

    def test_weekly_income_with_travel(self):
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date1)
        self.assertEqual(weekly_instance.income, 1000)

        Travel.objects.create(courier = self.courier, value=1000, date = self.date1)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date1)
        self.assertEqual(weekly_instance.income, 2000)

        Travel.objects.create(courier = self.courier, value=500, date = self.date2)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date1)
        self.assertEqual(weekly_instance.income, 2500) 

        Travel.objects.create(courier = self.courier, value=500, date = self.date4)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date1)
        self.assertEqual(weekly_instance.income, 2500) 
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date3)
        self.assertEqual(weekly_instance.income, 500) 

        Travel.objects.create(courier = self.courier, value=250, date = self.date4)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date1)
        self.assertEqual(weekly_instance.income, 2500) 
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date3)
        self.assertEqual(weekly_instance.income, 750) 



    def test_weekly_income_with_travel_bonus_penalty(self):
        Travel.objects.create(courier = self.courier, value=250, date = self.date4)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date3)
        self.assertEqual(weekly_instance.income, 250) 

        bonus = Bonus.objects.create(courier = self.courier, value=500, date = self.date3)

        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date3)
        self.assertEqual(weekly_instance.income, 750) 

        bonus.value = 450
        bonus.save()
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date3)
        self.assertEqual(weekly_instance.income, 700) 

        penalty = Penalty.objects.create(courier = self.courier, value=100, date = self.date4)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date3)
        self.assertEqual(weekly_instance.income, 600) 

        penalty.value = 50
        penalty.save()
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.date3)
        self.assertEqual(weekly_instance.income, 650) 

    def test_weekly_income_table_rows(self):
        Travel.objects.create(courier = self.courier, value=1000, date = self.date2)
        Travel.objects.create(courier = self.courier, value=1000, date = self.date4)
        self.assertEqual(WeeklyIncome.objects.all().values().count(), 2) 