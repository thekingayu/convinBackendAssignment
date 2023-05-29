from django.urls import path

from myApp.views import GoogleCalendarInitView, GoogleCalendarRedirectView, home
urlpatterns = [
    path('', home),
    path('rest/v1/calendar/init/', GoogleCalendarInitView),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView)
]