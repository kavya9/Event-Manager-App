from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import*
from .serializers import *
from rest_framework import generics
from django.template import loader
from django.views.generic.list import ListView
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
import json
from .forms import *
import datetime

# Create your views here.
from eventManager.models import *
from eventManager.serializers import *

#rest api  views
class TeacherList(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

'''class RegisteredEvents(generics.ListAPIView):
    queryset = RegisteredEvents.objects.all()
    serializer_class = RegisteredEventsSerializer'''

#normal views
def index(request):
    template='eventManager/index.html'
    return render(request,template)

def TeacherLogin(request):
    template = 'eventManager/teacherLogin.html'
    return render(request, template)

'''def StudentLogin(request):
    template = 'eventManager/studentLogin.html'
    return render(request, template)'''

def AdminLogin(request):
    template='eventManager/adminLogin.html'
    return render(request,template)

class About(ListView):
    model=Teacher
    template_name="eventManager/aboutTheApp.html"

class FacultyList(ListView):
    model=Teacher
    template_name="eventManager/facultyList.html"
    context_object_name="faculty"

    def get_queryset(self):
        return Teacher.objects.filter(teacherDept=self.kwargs['dept'])

    def get_context_data(self, **kwargs):
        context = super(FacultyList, self).get_context_data(**kwargs)
        context['dept'] = self.kwargs['dept']
        return context


def teacherLoginForm(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            userName = request.POST.get('userName')
            password = request.POST.get('password')

            querySet=Teacher.objects.filter(teacherName=userName,teacherPassword=password)
            #converts query set to string in json format
            data=json.dumps([dict(item) for item in Teacher.objects.filter(teacherName=userName,teacherPassword=password).values('id','teacherName', 'teacherPassword')])

            return JsonResponse(data,safe=False)
            #else : return HttpResponseRedirect('teacherLoginForm'+str(querySet[0].id))
    #Get goes here
    return render(request,'eventManager/teacherLoginForm.html')

def teacherLoggedIn(request,id):
    template = 'eventManager/index.html'
    return render(request, template)

'''class detail(DetailView):
    model=Event
    template_name = 'eventManager/events.html'
    context_object_name = "events"'''

def teacherOptions(request,pk):
    querySet = Event.objects.filter(id=pk)
    template = 'eventManager/teacherOptions.html'
    return render(request, template)

class CreateEvent(View):

    form_class = EventForm
    template_name = 'eventManager/eventForm.html'

    def get(self, request,id):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request,id):
        form = self.form_class(request.POST)

        if form.is_valid():
            # creats an object of form but doesnot save into database
            event = form.save(commit=False)
            # cleaned (normalized) data

            eventName = form.cleaned_data['eventName']
            resourcePerson = form.cleaned_data['resourcePerson']
            eventVenue = form.cleaned_data['eventVenue']
            ECE = form.cleaned_data['ECE']
            CSE = form.cleaned_data['CSE']
            EEE = form.cleaned_data['EEE']
            IT = form.cleaned_data['IT']
            mechanical = form.cleaned_data['mechanical']
            chemical = form.cleaned_data['chemical']
            civil = form.cleaned_data['civil']
            eventDate = form.cleaned_data['eventDate']

            todayDate=datetime.datetime.now().date()
            if(eventDate<=todayDate):
                return redirect('/eventManager/teacherLogin/%i/createEvent/invalidDate/' % int(id))

            eventStartTime = form.cleaned_data['eventStartTime']
            eventEndTime = form.cleaned_data['eventEndTime']
            if(eventStartTime>=eventEndTime):
                return redirect('/eventManager/teacherLogin/%i/createEvent/invalidTime/' % int(id))

            t=Teacher.objects.filter(id=self.kwargs['id'])

            event.teacher=t[0]

            event.save()

            #return redirect('eventDetail/%i/' % event.id)
            return redirect('/eventManager/teacherLogin/%i/createEvent/createEventSuccess/' % int(id))
        return redirect('/eventManager/teacherLogin/%i/createEvent/createEventFailure/' % int(id))

class InvalidTime(ListView):
    model=Event
    template_name='eventManager/invalidTime.html'

    def get_context_data(self, **kwargs):
        context = super(InvalidTime, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class InvalidDate(ListView):
    model=Event
    template_name='eventManager/invalidDate.html'

    def get_context_data(self, **kwargs):
        context = super(InvalidDate, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class CreateEventSuccess(ListView):
    model=Teacher
    template_name='eventManager/createEventSuccess.html'

    def get_context_data(self, **kwargs):
        context = super(CreateEventSuccess, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class CreateEventFailure(ListView):
    model=Teacher
    template_name='eventManager/createEventFailure.html'

    def get_context_data(self, **kwargs):
        context = super(CreateEventFailure, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class viewMyEvents(ListView):
    model=Event
    template_name="eventManager/viewMyEvents.html"
    context_object_name="myEvents"

    def get_queryset(self):
        return Event.objects.filter(teacher_id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(viewMyEvents, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class viewAllEvents(ListView):
    model=Event
    template_name="eventManager/viewAllEvents.html"
    context_object_name="allEvents"

    def get_queryset(self):
        return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super(viewAllEvents, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class ViewDetailsT(ListView):

    model = Teacher
    template_name = 'eventManager/viewDetailsT.html'
    context_object_name = "teacher"

    def get_queryset(self):
        return Teacher.objects.filter(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(ViewDetailsT, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

#student
def StudentLogin(request):
    if request.method == 'POST':
        # POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            userName = request.POST.get('userName')
            password = request.POST.get('password')

            querySet = Teacher.objects.filter(teacherName=userName, teacherPassword=password)
            # converts query set to string in json format
            data = json.dumps([dict(item) for item in
                               Student.objects.filter(studentRollNumber=userName, studentPassword=password).values('id',
                                                                                                             'studentName',
                                                                                                             'studentPassword')])

            return JsonResponse(data, safe=False)
            # else : return HttpResponseRedirect('teacherLoginForm'+str(querySet[0].id))
    # Get goes here
    return render(request, 'eventManager/studentLogin.html')

def studentOptions(request,pk):
    querySet = Event.objects.filter(id=pk)
    template = 'eventManager/studentOptions.html'
    return render(request, template)

class viewMyDeptEvents(ListView):
    model=Event
    template_name="eventManager/viewMyDeptEvents.html"
    context_object_name="myEvents"

    def get_queryset(self):
        q=Student.objects.filter(id=self.kwargs['id']).values('studentDept')
        s=q[0].values()
        dept=s[0].encode('iso-8859-1')
        if(dept=='CSE'):
            return Event.objects.filter(CSE=True)
        if (dept == 'ECE'):
            return Event.objects.filter(ECE=True)
        if (dept == 'EEE'):
            return Event.objects.filter(EEE=True)
        if (dept == 'IT'):
            return Event.objects.filter(IT=True)
        if (dept == 'mechanical'):
            return Event.objects.filter(mechanical=True)
        if (dept == 'chemical'):
            return Event.objects.filter(chemical=True)
        if (dept == 'civil'):
            return Event.objects.filter(civil=True)

    def get_context_data(self, **kwargs):
        context = super(viewMyDeptEvents, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class viewAllEventsS(ListView):
    model=Event
    template_name="eventManager/viewAllEventsS.html"
    context_object_name="allEvents"

    def get_queryset(self):
        return Event.objects.all()

    def get_context_data(self, **kwargs):
        context = super(viewAllEventsS, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class viewMyEventsS(ListView):
    model=Event
    template_name="eventManager/viewMyEventsS.html"
    context_object_name="myEvents"

    def get_queryset(self):
        eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).values('event')
        l = []
        for p in eve:
            l.append(p.values()[0])
        r = Event.objects.filter(id__in=l)
        return r

    def get_context_data(self, **kwargs):
        context = super(viewMyEventsS, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context



class registerEvent(ListView):
    model = Event
    template_name = "eventManager/registerEvent.html"
    context_object_name = "myEvents"

    def get_queryset(self):
        q = Student.objects.filter(id=self.kwargs['id']).values('studentDept')
        s = q[0].values()
        dept = s[0].encode('iso-8859-1')
        todayDate=datetime.datetime.now().date()
        if (dept == 'CSE'):
            eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).values('event')
            l = []
            for p in eve:
                l.append(p.values()[0])
            r = Event.objects.filter(CSE=True).filter(eventDate__gt=todayDate).exclude(id__in=l)
            return r

        if (dept == 'ECE'):
            eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).values('event')
            l=[]
            for p in eve:
                l.append(p.values()[0])
            r = Event.objects.filter(ECE=True).filter(eventDate__gt=todayDate).exclude(id__in=l)
            return r

        if (dept == 'EEE'):
            eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).values('event')
            l = []
            for p in eve:
                l.append(p.values()[0])
            r = Event.objects.filter(EEE=True).filter(eventDate__gt=todayDate).exclude(id__in=l)
            return r

        if (dept == 'IT'):
            eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).values('event')
            l = []
            for p in eve:
                l.append(p.values()[0])
            r = Event.objects.filter(IT=True).filter(eventDate__gt=todayDate).exclude(id__in=l)
            return r

        if (dept == 'mechanical'):
            eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).values('event')
            l = []
            for p in eve:
                l.append(p.values()[0])
            r = Event.objects.filter(mechanical=True).filter(eventDate__gt=todayDate).exclude(id__in=l)
            return r

        if (dept == 'chemical'):
            eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).values('event')
            l = []
            for p in eve:
                l.append(p.values()[0])
            r = Event.objects.filter(chemical=True).filter(eventDate__gt=todayDate).exclude(id__in=l)
            return r

        if (dept == 'civil'):
            eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).values('event')
            l = []
            for p in eve:
                l.append(p.values()[0])
            r = Event.objects.filter(civil=True).filter(eventDate__gt=todayDate).exclude(id__in=l)
            return r

    def get_context_data(self, **kwargs):
        context = super(registerEvent, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class eventRegistered(ListView):
    model=Event
    template_name = 'eventManager/eventRegistered.html'
    context_object_name = "events"

    def get_queryset(self):
        students=Event.objects.filter(id=self.kwargs['eid']).values('studentsRegistered')
        number=students[0].values()[0]
        number=number+1
        Event.objects.filter(id=self.kwargs['eid']).update(studentsRegistered=number)
        r=RegisteredEvents.objects.create(event_id=self.kwargs['eid'],student_id=self.kwargs['id'])
        return Event.objects.filter(id=self.kwargs['eid'])

    def get_context_data(self, **kwargs):
        context = super(eventRegistered, self).get_context_data(**kwargs)
        context['id']=self.kwargs['id']
        return context



class GiveFeedback(ListView):
    model = RegisteredEvents
    template_name = "eventManager/givefeedback.html"
    context_object_name = "myEvents"

    def get_queryset(self):
        eve = RegisteredEvents.objects.filter(student=Student.objects.filter(id=self.kwargs['id'])).filter(eventRating=0).values('event')
        l = []
        for p in eve:
            l.append(p.values()[0])
        r = Event.objects.filter(id__in=l)
        return r

    def get_context_data(self, **kwargs):
        context = super(GiveFeedback, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context


class Feedback(View):
    form_class = FeedbackForm
    template_name = 'eventManager/feedBackForm.html'


    # display blank form
    def get(self, request,id,eid):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process data
    def post(self, request,id,eid):
        form = self.form_class(request.POST)
        if form.is_valid():
            regEve = form.save(commit=False)
            eventRating = form.cleaned_data['eventRating']
            teacherCredits=form.cleaned_data['teacherCredits']
            eventName = Event.objects.filter(id=self.kwargs['eid'])
            studentName=Student.objects.filter(id=self.kwargs['id'])
            re=RegisteredEvents.objects.filter(event=eventName[0],student=studentName[0])
            re1=re[0]
            re1.eventRating = eventRating
            re1.teacherCredits=teacherCredits
            re1.save()

            event=eventName[0]
            studentsReg=event.studentsRegistered
            eventRa=event.eventRating
            event.eventRating=(((studentsReg-1)*eventRa)+eventRating)/studentsReg
            event.save()

            t=event.teacher
            #id1=teacher.values()[0]
            #t=Teacher.objects.filter(id=id1)
            t.teacherCredits=teacherCredits
            t.save()

            return redirect('/eventManager/studentLogin/%i/feedbackSuccess' % int(id))
        return redirect('/eventManager/studentLogin/%i/givefeedback/invalidFeedback' % int(id))

class InvalidFeedback(ListView):
    model=Event
    template_name='eventManager/invalidFeedback.html'

    def get_context_data(self, **kwargs):
        context = super(InvalidFeedback, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class FeedbackSuccess(ListView):
    model=Event
    template_name='eventManager/feedbackSuccess.html'

    def get_context_data(self, **kwargs):
        context = super(FeedbackSuccess, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class ViewDetailsS(ListView):
    model=Student
    template_name = 'eventManager/viewDetailsS.html'
    context_object_name = "student"

    def get_queryset(self):
        return Student.objects.filter(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(ViewDetailsS, self).get_context_data(**kwargs)
        context['id']=self.kwargs['id']
        return context


#admin

def adminLoginForm(request):
    if request.method == 'POST':
        #POST goes here . is_ajax is must to capture ajax requests. Beginner's pit.
        if request.is_ajax():
            userName = request.POST.get('userName')
            password = request.POST.get('password')

            querySet=Admin.objects.filter(adminName=userName,adminPassword=password)
            #converts query set to string in json format
            data=json.dumps([dict(item) for item in Admin.objects.filter(adminName=userName,adminPassword=password).values('id','adminName', 'adminPassword')])

            return JsonResponse(data,safe=False)
            #else : return HttpResponseRedirect('teacherLoginForm'+str(querySet[0].id))
    #Get goes here
    return render(request,'eventManager/adminLoginForm.html')

def adminOptions(request,pk):
    template = 'eventManager/adminOptions.html'
    return render(request, template)

class RegisterTeacher(View):
    form_class = TeacherForm
    template_name = 'eventManager/registerTeacher.html'

    # display blank form
    def get(self, request,id):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process data
    def post(self, request,id):
        form = self.form_class(request.POST)

        if form.is_valid():
            # creats an object of form but doesnot save into database
            teacher = form.save(commit=False)
            teacherName = form.cleaned_data['teacherName']
            teacherPassword = form.cleaned_data['teacherPassword']
            teacherDepartment = form.cleaned_data['teacherDept']
            teacherExperience = form.cleaned_data['teacherExperience']

            q = Teacher.objects.filter(teacherName=teacherName,teacherDept=teacherDepartment)
            if q.__len__() != 0: return redirect('/eventManager/adminLogin/%i/registerTeacher/teacherAlreadyExists/' % int(id))

            d=["CSE","ECE","EEE","IT","mechanical","chemical","civil"]
            if(teacherDepartment not in d):
                return redirect('/eventManager/adminLogin/%i/registerTeacher/teacherinvalidDept/' % int(id))

            teacher.save()

            return redirect('/eventManager/adminLogin/%i/registerTeacher/teacherRegisterSuccess/' % int(id))
        return redirect('/eventManager/adminLogin/%i/registerTeacher/teacherRegisterFailure/' % int(id))

class TeacherRegisterSuccess(ListView):
    model=Teacher
    template_name='eventManager/teacherRegisterSuccess.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherRegisterSuccess, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class TeacherRegisterFailure(ListView):
    model=Teacher
    template_name='eventManager/teacherRegisterFailure.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherRegisterFailure, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class TeacherAlreadyExists(ListView):
    model=Teacher
    template_name='eventManager/teacherAlreadyExists.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherAlreadyExists, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class TeacherInvalidDept(ListView):
    model=Teacher
    template_name='eventManager/teacherInvalidDept.html'

    def get_context_data(self, **kwargs):
        context = super(TeacherInvalidDept, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class RegisterStudent(View):
    form_class = StudentForm
    template_name = 'eventManager/registerStudent.html'

    # display blank form
    def get(self, request,id):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process data
    def post(self, request,id):
        form = self.form_class(request.POST)

        if form.is_valid():
            # creats an object of form but doesnot save into database
            student = form.save(commit=False)
            studentName = form.cleaned_data['studentName']
            studentPassword = form.cleaned_data['studentPassword']
            studentDepartment = form.cleaned_data['studentDept']
            studentRollNumber = form.cleaned_data['studentRollNumber']

            q = Student.objects.filter(studentRollNumber=studentRollNumber)
            if q.__len__()!=0:return redirect('/eventManager/adminLogin/%i/registerStudent/studentAlreadyExists/' % int(id))

            d = ["CSE", "ECE", "EEE", "IT", "mechanical", "chemical", "civil"]
            if (studentDepartment not in d):
                return redirect('/eventManager/adminLogin/%i/registerStudent/studentinvalidDept/' % int(id))

            studentCGPA = form.cleaned_data['studentCGPA']
            studentAttendance = form.cleaned_data['studentAttendance']

            student.save()

            return redirect('/eventManager/adminLogin/%i/registerStudent/studentRegisterSuccess/' % int(id))
        return redirect('/eventManager/adminLogin/%i/registerStudent/studentRegisterFailure/' % int(id))

class StudentRegisterSuccess(ListView):
    model=Student
    template_name='eventManager/studentRegisterSuccess.html'

    def get_context_data(self, **kwargs):
        context = super(StudentRegisterSuccess, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class StudentRegisterFailure(ListView):
    model=Student
    template_name='eventManager/studentRegisterFailure.html'

    def get_context_data(self, **kwargs):
        context = super(StudentRegisterFailure, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context


class StudentAlreadyExists(ListView):
    model=Teacher
    template_name='eventManager/studentAlreadyExists.html'

    def get_context_data(self, **kwargs):
        context = super(StudentAlreadyExists, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

class StudentInvalidDept(ListView):
    model=Teacher
    template_name='eventManager/studentInvalidDept.html'

    def get_context_data(self, **kwargs):
        context = super(StudentInvalidDept, self).get_context_data(**kwargs)
        context['id'] = self.kwargs['id']
        return context

