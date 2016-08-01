from django.conf.urls import url, include
from . import views
from django.contrib import admin

app_name='eventManager'

urlpatterns=[
    #rest-api urls
    url(r'^teachers/$', views.TeacherList.as_view()),
    url(r'^students/$', views.StudentList.as_view()),
    url(r'^teachers/(?P<pk>[0-9]+)/$', views.EventDetail.as_view()),
    #url(r'^students/(?P<pk>[0-9]+)/$', views.RegisteredEvents.as_view()),
    #normal urls
    url(r'^$',views.index,name="index"),
    url(r'^teacherLogin/$',views.TeacherLogin,name="teacherLogin"),
    url(r'^studentLogin/$',views.StudentLogin,name="studentLogin"),
    url(r'^teacherLogin/teacherLoginForm',views.teacherLoginForm,name="teacherLoginForm"),
   # url(r'^teacherLogin/(?P<pk>[0-9]+)$', views.teacherLoggedIn, name="teacherLoggedIn"),
    url(r'^admin/adminLogin', views.AdminLogin, name="adminLogin"),
    #url(r'^admin/adminLogin/teacherRegister/$',views.TeacherFormView,name="teacherRegister"),
   # url(r'^ajaxtest/$',views.ajaxtest,name="test"),
    #url(r'^teacherLogin/(?P<pk>[0-9]+)$', views.detail.as_view(), name="teacherLoggedIn"),
    url(r'^teacherLogin/(?P<pk>[0-9]+)/$', views.teacherOptions, name="teacherOptions"),
    url(r'^teacherLogin/(?P<id>[0-9]+)/createEvent/$', views.CreateEvent.as_view(), name="createEvent"),
    url(r'^teacherLogin/(?P<id>[0-9]+)/viewMyEvents/$', views.viewMyEvents.as_view(), name="viewMyEvents"),
    url(r'^teacherLogin/(?P<id>[0-9]+)/viewAllEvents/$', views.viewAllEvents.as_view(), name="viewAllEvents"),

    url(r'^teacherLogin/(?P<dept>[a-zA-Z]+)/facultyList/$',views.FacultyList.as_view(),name="facultyList"),
    url(r'^teacherLogin/(?P<id>[0-9]+)/viewDetailsT/$', views.ViewDetailsT.as_view(), name="viewDetailsT"),
    url(r'^teacherLogin/(?P<id>[0-9]+)/createEvent/invalidTime/$', views.InvalidTime.as_view(), name="invalidTime"),
    url(r'^teacherLogin/(?P<id>[0-9]+)/createEvent/invalidDate/$', views.InvalidDate.as_view(), name="invalidDate"),
    url(r'^teacherLogin/(?P<id>[0-9]+)/createEvent/createEventSuccess/$', views.CreateEventSuccess.as_view(), name="createEventSuccess"),
    url(r'^teacherLogin/(?P<id>[0-9]+)/createEvent/createEventFailure/$', views.CreateEventFailure.as_view(), name="createEventFailure"),
    url(r'^about/$',views.About.as_view(),name="about"),

    #students
    url(r'^studentLogin/$',views.StudentLogin,name="studentLogin"),
    url(r'^studentLogin/(?P<pk>[0-9]+)/$', views.studentOptions, name="studentOptions"),
    url(r'^studentLogin/(?P<id>[0-9]+)/viewAllEventsS/$', views.viewAllEventsS.as_view(), name="viewAllEventsS"),
    url(r'^studentLogin/(?P<id>[0-9]+)/viewMyDeptEvents/$', views.viewMyDeptEvents.as_view(), name="viewMyDeptEvents"),
    url(r'^studentLogin/(?P<id>[0-9]+)/viewMyEventsS/$', views.viewMyEventsS.as_view(), name="viewMyEventsS"),
    url(r'^studentLogin/(?P<id>[0-9]+)/registerEvent/$', views.registerEvent.as_view(), name="registerEvent"),
    url(r'^studentLogin/(?P<id>[0-9]+)/registerEvent/(?P<eid>[0-9]+)/$', views.eventRegistered.as_view(), name="eventRegistered"),
    url(r'^studentLogin/(?P<id>[0-9]+)/givefeedback/(?P<eid>[0-9]+)/$', views.Feedback.as_view(), name="feedback"),
    url(r'^studentLogin/(?P<id>[0-9]+)/givefeedback/$', views.GiveFeedback.as_view(), name="givefeedback"),
    url(r'^studentLogin/(?P<id>[0-9]+)/givefeedback/invalidFeedback$', views.InvalidFeedback.as_view(), name="invalidFeedback"),
    url(r'^studentLogin/(?P<id>[0-9]+)/feedbackSuccess/$', views.FeedbackSuccess.as_view(), name="feedbackSuccess"),
    url(r'^studentLogin/(?P<id>[0-9]+)/viewDetailsS/$', views.ViewDetailsS.as_view(), name="viewDetailsS"),

    #admin
    url(r'^adminLogin/$', views.adminLoginForm, name="adminLogin"),
    url(r'^adminLogin/(?P<pk>[0-9]+)/$', views.adminOptions, name="adminOptions"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerTeacher/$', views.RegisterTeacher.as_view(), name="registerTeacher"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerTeacher/teacherRegisterSuccess/$', views.TeacherRegisterSuccess.as_view(), name="teacherRegisterSuccess"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerTeacher/teacherRegisterFailure/$', views.TeacherRegisterFailure.as_view(),name="teacherRegisterFailure"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerTeacher/teacherinvalidDept/$', views.TeacherInvalidDept.as_view(),name="teacherinvalidDept"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerTeacher/teacherAlreadyExists/$', views.TeacherAlreadyExists.as_view(),name="teacherAlreadyExists"),

    url(r'^adminLogin/(?P<id>[0-9]+)/registerStudent/$', views.RegisterStudent.as_view(), name="registerStudent"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerStudent/studentRegisterSuccess/$', views.StudentRegisterSuccess.as_view(),name="studentRegisterSuccess"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerStudent/studentRegisterFailure/$', views.StudentRegisterFailure.as_view(),name="studentRegisterFailure"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerStudent/studentAlreadyExists/$', views.StudentAlreadyExists.as_view(),name="studentAlreadyExists"),
    url(r'^adminLogin/(?P<id>[0-9]+)/registerStudent/studentinvalidDept/$', views.StudentInvalidDept.as_view(), name="StudentinvalidDept"),

]