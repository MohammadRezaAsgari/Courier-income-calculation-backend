from django.urls import path
from .views import *

urlpatterns = [
    path('weekly-incomes/', WeeklyIncomeListView.as_view()),
]
