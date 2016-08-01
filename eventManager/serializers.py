from django.core.serializers import serialize
from rest_framework import serializers
from eventManager.models import *


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields='__all__'

class RegisteredEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredEvents
        fields='__all__'