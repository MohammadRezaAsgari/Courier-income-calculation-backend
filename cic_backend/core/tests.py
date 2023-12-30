from django.test import TestCase
from .models import Courier, Travel, Bonus, Penalty, DailyIncome, WeeklyIncome
from datetime import datetime

class DailyIncomeTestCase(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(first_name='courier1_first_name',last_name='courier1_last_name')
        self.first_date = datetime.strptime('2023-12-08', '%Y-%m-%d')

        Travel.objects.create(courier = self.courier, value=1000, date = self.first_date)

    def test_daily_income_with_travel(self):
        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.first_date)
        self.assertEqual(daily_instance.income, 1000)

        Travel.objects.create(courier = self.courier, value=500, date = self.first_date)
        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.first_date)        
        self.assertEqual(daily_instance.income, 1500)


    def test_daily_income_with_travel_bonus_penalty(self):
        Bonus.objects.create(courier = self.courier, value=500, date = self.first_date)

        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.first_date)
        self.assertEqual(daily_instance.income, 1500)

        Penalty.objects.create(courier = self.courier, value=100, date = self.first_date)

        daily_instance = DailyIncome.objects.get(courier = self.courier, date = self.first_date)
        self.assertEqual(daily_instance.income, 1400)



class WeeklyIncomeTestCase(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(first_name='courier1_first_name',last_name='courier1_last_name')

        self.first_date = datetime.strptime('2023-12-02', '%Y-%m-%d')# <-- the date is saturday
        self.second_date = datetime.strptime('2023-12-05', '%Y-%m-%d')# <-- the last saturday is 2023-12-02
        self.third_date = datetime.strptime('2023-12-07', '%Y-%m-%d')# <-- the last saturday is 2023-12-02

        self.fourth_date = datetime.strptime('2023-12-09', '%Y-%m-%d')# <-- the date is saturday
        self.fifth_date = datetime.strptime('2023-12-13', '%Y-%m-%d')# <-- the last saturday is 2023-12-09
        

        Travel.objects.create(courier = self.courier, value=1000, date = self.first_date)

    def test_weekly_income_with_travel(self):
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.first_date)
        self.assertEqual(weekly_instance.income, 1000)

        Travel.objects.create(courier = self.courier, value=1000, date = self.first_date)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.first_date)
        self.assertEqual(weekly_instance.income, 2000)

        Travel.objects.create(courier = self.courier, value=500, date = self.first_date)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.first_date)
        self.assertEqual(weekly_instance.income, 2500) 

        Travel.objects.create(courier = self.courier, value=500, date = self.third_date)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.first_date)
        self.assertEqual(weekly_instance.income, 3000) 

        Travel.objects.create(courier = self.courier, value=500, date = self.fourth_date)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.first_date)
        self.assertEqual(weekly_instance.income, 3000) 
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.fourth_date)
        self.assertEqual(weekly_instance.income, 500) 

        Travel.objects.create(courier = self.courier, value=250, date = self.fifth_date)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.first_date)
        self.assertEqual(weekly_instance.income, 3000) 
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.fourth_date)
        self.assertEqual(weekly_instance.income, 750) 

        self.assertEqual(WeeklyIncome.objects.all().values().count(), 2) 

    def test_weekly_income_with_travel_bonus_penalty(self):
        Travel.objects.create(courier = self.courier, value=250, date = self.fifth_date)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.fourth_date)
        self.assertEqual(weekly_instance.income, 250) 

        Bonus.objects.create(courier = self.courier, value=500, date = self.fourth_date)

        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.fourth_date)
        self.assertEqual(weekly_instance.income, 750) 

        Penalty.objects.create(courier = self.courier, value=100, date = self.fifth_date)
        weekly_instance = WeeklyIncome.objects.get(courier = self.courier, saturday_date = self.fourth_date)
        self.assertEqual(weekly_instance.income, 650) 
