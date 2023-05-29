# ConvinBackendAssignment
Convin Backend Assignment
# Problem Statement
In this assignment you have to implement google calendar integration using django rest api. You need to use the OAuth2 mechanism to get users calendar access. Below are detail of API endpoint and corresponding views which you need to implement /rest/v1/calendar/init/ -> GoogleCalendarInitView()
This view should start step 1 of the OAuth. Which will prompt user for
his/her credentials
/rest/v1/calendar/redirect/ -> GoogleCalendarRedirectView()
This view will do two things
1. Handle redirect request sent by google with code for token. You
need to implement mechanism to get access_token from given
code
2. Once got the access_token get list of events in users calendar

# Solution Steps

1. Create a new Django project and app.
2. Install the google-api-python-client package.
3. Create a GoogleCalendarInitView class. This class will handle the initial authorization request from the user.
4. Create a GoogleCalendarEventsView class. This class will handle the request to get the list of events from the user's calendar.
5. Configure the OAuth2 flow in your Django project.
6. Test the integration by making a request to the /rest/v1/calendar/init/ endpoint.

# Here is the python code for the GoogleCalendarInitView class:

from django.views.generic import View
from django.http import HttpResponseRedirect
from oauth2client.client import OAuth2WebServerFlow


class GoogleCalendarInitView(View):
    """
    View to handle the initial authorization request from the user.
    """

    def get(self, request):
        # Create the OAuth2 flow.
        flow = OAuth2WebServerFlow(
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scope='https://www.googleapis.com/auth/calendar',
            redirect_uri=settings.GOOGLE_REDIRECT_URI,
        )

        # Redirect the user to the authorization URL.
        return HttpResponseRedirect(flow.step1_get_authorize_url())

# Here is the python code for the GoogleCalendarEventsView class:

from django.views.generic import View
from django.http import HttpResponse
from oauth2client.client import OAuth2Credentials


class GoogleCalendarEventsView(View):
    """
    View to handle the request to get the list of events from the user's calendar.
    """

    def get(self, request):
        # Get the OAuth2 credentials from the request.
        credentials = OAuth2Credentials.get_from_request(request)

        # Create the Google Calendar service object.
        service = py_gcal.CalendarService(credentials=credentials)

        # Get the list of events from the user's calendar.
        events = service.events().list().execute()

        # Return the list of events as JSON.
        return HttpResponse(json.dumps(events, indent=4), content_type='application/json')

# Here is the python code to configure the OAuth2 flow in your Django project:

from django.conf import settings

flow = OAuth2WebServerFlow(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/calendar',
    redirect_uri=settings.GOOGLE_REDIRECT_URI,
)

settings.GOOGLE_FLOW = flow

To test the integration, make a request to the /rest/v1/calendar/init/ endpoint. You will be redirected to a Google page where you can authorize the application to access your calendar. Once you have authorized the application, you will be redirected back to your application. The response will contain a JSON object with the access token. You can then use the access token to make requests to the Google Calendar API.
