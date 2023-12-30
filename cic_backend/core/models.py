from django.db import models


class Courier(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        unique_together = ['first_name','last_name']

class Travel(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    date = models.DateField()

class Bonus(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    date = models.DateField()

class Penalty(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()
    date = models.DateField()

class DailyIncome(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    income = models.IntegerField(default=0)
    date = models.DateField()

class WeeklyIncome(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    income = models.IntegerField(default=0)
    saturday_date = models.DateField()
