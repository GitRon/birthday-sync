import datetime

from django.conf import settings
from googleapiclient.discovery import build

from birthday_sync.services.google.authenticate import authenticate


class GoogleEventService:  # noqa: PBR005
    calendar_id = settings.BIRTHDAY_CALENDAR_ID
    google_service = None

    def __init__(self):
        super().__init__()

        # Authenticate at Google
        creds = authenticate()

        # Google Calendar API aufrufen
        self.google_service = build("calendar", "v3", credentials=creds)

    def _get_body(self, *, summary: str, target_date: datetime.date) -> dict:
        return {
            "summary": summary,
            "birthday": "birthday",
            "status": "confirmed",
            "start": {
                "date": target_date.isoformat(),
            },
            "end": {
                "date": target_date.isoformat(),
            },
            "recurrence": [
                "RRULE:FREQ=YEARLY",
            ],
            # todo: find a way to set useful reminders
            # "reminders": {
            #     "useDefault": False,
            #     "overrides": [
            #         {"method": "popup", "minutes": 960},
            #     ],
            # },
        }

    def create_event(self, *, summary: str, target_date: datetime.date) -> str:
        event = self._get_body(summary=summary, target_date=target_date)

        # Termin in den Hauptkalender einfügen
        event = (
            self.google_service.events()
            .insert(calendarId=self.calendar_id, body=event)
            .execute()
        )

        return event["id"]

    def update_event(self, *, event_id: str, summary: str, target_date: datetime.date):
        self.google_service.events().update(
            calendarId=self.calendar_id,
            eventId=event_id,
            body=self._get_body(summary=summary, target_date=target_date),
        ).execute()

    def delete_event(self, *, event_id: str):
        self.google_service.events().delete(
            calendarId=self.calendar_id, eventId=event_id
        ).execute()
