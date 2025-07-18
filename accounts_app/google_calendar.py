from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = settings.GOOGLE_SERVICE_ACCOUNT_FILE


def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # If credentials are expired, refresh them
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    service = build('calendar', 'v3', credentials=credentials)
    return service


def create_calendar_event(appointment, doctor_email):
    service = get_calendar_service()

    event = {
        'summary': f'Appointment with {appointment.patient.first_name} {appointment.patient.last_name}',
        'start': {
            'dateTime': appointment.start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Kolkata',  # Set your timezone
        },
        'end': {
            'dateTime': appointment.end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Kolkata',  # Set your timezone
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},  # 24 hours before
                {'method': 'popup', 'minutes': 30},      # 30 minutes before
            ],
        },
    }

    # Insert the event into Doctor's calendar
    event = service.events().insert(calendarId=doctor_email, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
