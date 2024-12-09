from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, Resource
import datetime
import os
from dotenv import load_dotenv
from logger import logger

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']
TODAY = datetime.date.today()

class GoogleCalendarAPI:
    def __init__(self, credentials_file: str, calendar_id: str):
        self.credentials: Credentials = Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES
        )
        self.service: Resource = build('calendar', 'v3', credentials=self.credentials)
        self.calendar_id = calendar_id
        logger.info("Google Calendar API initialized")

    def add_event_full_day(self, name: str, description: str = "", day: int = None, month: int = None, year: int = None) -> bool:
        """Add a full-day event to the calendar."""
        if day is None:
            day = TODAY.day
        if month is None:
            month = TODAY.month
        if year is None:
            year = TODAY.year

        event = {
            'summary': name,
            'description': description,
            'start': {'date': datetime.date(year, month, day).isoformat()},
            'end': {'date': (datetime.date(year, month, day) + datetime.timedelta(days=1)).isoformat()},
        }

        try:
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            logger.info(f"Event created: {event['htmlLink']}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return False
        return True

    def add_event_with_time(self, name: str, starthour: int, startminute: int, endhour: int, endminute: int, description: str = "", day: int = None, month: int = None, year: int = None) -> bool:
        """Add a partial-day event to the calendar."""
        if day is None:
            day = TODAY.day
        if month is None:
            month = TODAY.month
        if year is None:
            year = TODAY.year

        start_datetime = datetime.datetime(year, month, day, starthour, startminute)
        end_datetime = datetime.datetime(year, month, day, endhour, endminute)
        event = {
            'summary': name,
            'description': description,
            'start': {'dateTime': start_datetime.isoformat()},
            'end': {'dateTime': end_datetime.isoformat()},
        }

        try:
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            logger.info(f"Event created: {event['htmlLink']}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return False
        return True

    def add_multi_day_event(self, name: str, description: str, startday: int, startmonth: int, startyear: int, endday: int, endmonth: int, endyear: int) -> bool:
        """Add a multi-day event to the calendar."""
        start_date = datetime.date(startyear, startmonth, startday).isoformat()
        end_date = (datetime.date(endyear, endmonth, endday) + datetime.timedelta(days=1)).isoformat()

        event = {
            'summary': name,
            'description': description,
            'start': {'date': start_date},
            'end': {'date': end_date},
        }

        try:
            event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
            logger.info(f"Event created: {event['htmlLink']}")
        except Exception as error:
            logger.error(f"Error: {error}")
            return False
        return True

    def get_events(self, startday: int = None, startmonth: int = None, startyear: int = None, endday: int = None, endmonth: int = None, endyear: int = None) -> list:
        """Retrieve all events from the calendar within a date range."""
        if startday is None:
            startday = TODAY.day
        if startmonth is None:
            startmonth = TODAY.month
        if startyear is None:
            startyear = TODAY.year
        if endday is None:
            endday = TODAY.day
        if endmonth is None:
            endmonth = TODAY.month
        if endyear is None:
            endyear = TODAY.year

        time_min = datetime.datetime(startyear, startmonth, startday).isoformat() + 'Z'
        time_max = datetime.datetime(endyear, endmonth, endday, 23, 59, 59).isoformat() + 'Z'

        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            logger.info("Events retrieved")
            return events
        except Exception as error:
            logger.error(f"Error: {error}")
            return []
