from rest_framework import serializers
from .models import WeeklyIncome,Courier

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'

class WeeklyIncomeSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True)
    class Meta:
        model = WeeklyIncome
        fields = '__all__'