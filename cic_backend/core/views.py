from rest_framework import generics
from .models import WeeklyIncome
from .serializers import WeeklyIncomeSerializer


class WeeklyIncomeListView(generics.ListAPIView):
    queryset = WeeklyIncome.objects.all()
    serializer_class = WeeklyIncomeSerializer
