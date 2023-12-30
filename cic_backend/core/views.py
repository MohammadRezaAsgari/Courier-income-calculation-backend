from rest_framework import generics
import django_filters
from .models import WeeklyIncome
from .serializers import WeeklyIncomeSerializer
from .filters import WeeklyIncomeFilter


class WeeklyIncomeListView(generics.ListAPIView):
    queryset = WeeklyIncome.objects.all()
    serializer_class = WeeklyIncomeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = WeeklyIncomeFilter