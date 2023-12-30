from django.contrib import admin
from .models import *

admin.site.register(Courier)
admin.site.register(Travel)
admin.site.register(Bonus)
admin.site.register(Penalty)
admin.site.register(DailyIncome)
admin.site.register(WeeklyIncome)
