from rest_framework import serializers
from .models import Schedule

# class will serialize the model fields specified data into JSON so it is easily readable by react


class ReactSerializer (serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['team', 'date', 'opponent', 'time', 'channel']
