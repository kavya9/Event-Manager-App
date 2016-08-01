from django.forms.models import ModelForm
from django import forms

from eventManager.models import *


class TeacherForm(ModelForm):
    class Meta:
        model=Teacher
        fields = ('teacherName',  'teacherPassword','teacherDept','teacherExperience')

class StudentForm(ModelForm):
    studentPassword = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Student
        fields=('studentRollNumber','studentName','studentPassword','studentDept','studentCGPA','studentAttendance')

class EventForm(ModelForm):
    class Meta:
        model=Event
        fields=('eventName','resourcePerson','eventDate','eventStartTime','eventEndTime','eventVenue','ECE','CSE','EEE','IT','mechanical','chemical','civil')

class FeedbackForm(ModelForm):
    class Meta:
        model = RegisteredEvents
        fields = ('eventRating','teacherCredits')

class AdminForm(ModelForm):
    adminPassword=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Admin
        fields=('adminName','adminPassword')