import django_filters
from .models import WeeklyIncome

class WeeklyIncomeFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name="saturday_date", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="saturday_date", lookup_expr="lte")

    class Meta:
        model = WeeklyIncome
        fields = ['saturday_date']