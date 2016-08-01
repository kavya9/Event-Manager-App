from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

# Create your models here.
from django.forms.models import ModelForm


class Teacher(models.Model):
    teacherName = models.CharField(max_length=100)
    teacherDept=models.CharField(max_length=100)
    teacherExperience=models.PositiveIntegerField()
    teacherPassword=models.CharField(default="anits123*",max_length=25)
    teacherCredits=models.FloatField(default=0.0)

    def __str__(self):
        return self.teacherName

class Event(models.Model):
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    eventName=models.CharField(max_length=100)
    resourcePerson=models.CharField(max_length=200)
    eventDate=models.DateField()
    eventStartTime=models.TimeField() #'hh-mm-ss' or 'hh-mm' and 24 hr format
    eventEndTime=models.TimeField()
    eventVenue=models.CharField(max_length=200)
    eventRating=models.FloatField(default=0.0)
    studentsRegistered=models.IntegerField(default=0)
    ECE = models.BooleanField(default=False)
    CSE = models.BooleanField(default=False)
    EEE = models.BooleanField(default=False)
    IT = models.BooleanField(default=False)
    mechanical = models.BooleanField(default=False)
    chemical = models.BooleanField(default=False)
    civil=models.BooleanField(default=False)
    timesViewed=models.IntegerField(default=0)

    def __str__(self):
        return self.eventName

    def get_absolute_url(self):
        return reverse('eventManager:eventDetail',kwargs={'pk':self.id})

#actual student for batch 2013-17(ANITS) in inserted from student-Master-Data-2017.xlsx to DB in studentMasterDataExcelToDb.py located in same directory
class Student(models.Model):
    studentName=models.CharField(max_length=100)
    studentRollNumber=models.CharField(max_length=12)#,validators=[RegexValidator('r^31\d{2}265\d{5}$')])
    studentDept=models.CharField(max_length=100)
    studentPassword=models.CharField(default="anits123*",max_length=25)
    studentCGPA=models.FloatField(default=0.0,validators=[MinValueValidator(0.0),MaxValueValidator(10.0)])
    studentAttendance=models.FloatField(default=0.0,validators=[MinValueValidator(0.0),MaxValueValidator(100.0)])

    def __str__(self):
        return self.studentName

class RegisteredEvents(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    eventRating=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])
    teacherCredits=models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])

class Admin(models.Model):
    adminName=models.CharField(max_length=100)
    adminPassword=models.CharField(max_length=25)

    def __str__(self):
        return self.adminName











