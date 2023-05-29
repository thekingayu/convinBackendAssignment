from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
import os
import json
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@api_view()
def home(request):
    return JsonResponse({'message':'Welcome to Convin Google Calendar API', 'status':'200'})



@api_view()
def GoogleCalendarInitView(request):
    flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(CORE_DIR, "credentials.json"), SCOPES)
    creds = flow.run_local_server(port=8080)
    request.session['creds'] = creds.to_json()
    return redirect(GoogleCalendarRedirectView)

@api_view()
def GoogleCalendarRedirectView(request):
    try:
        creds = Credentials.from_authorized_user_info(json.loads(request.session.get('creds')), SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                return redirect(GoogleCalendarInitView)

        service = build('calendar', 'v3', credentials = creds)
        # Call the Calendar API
        
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return JsonResponse({'message':'No events found!', 'status':'404'})

        listEvents = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            listEvents.append({start : event['summary']})
        return JsonResponse(listEvents, safe=False)

    except HttpError as error:
        return HttpResponse('An error occurred: %s' % error)
     

