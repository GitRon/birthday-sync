import datetime

from django.core.management import BaseCommand
from django.utils import timezone

from birthday_sync.models import GoogleContact
from birthday_sync.services.google.contacts import sync_birthdays
from birthday_sync.services.google.events import GoogleEventService


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Fetch all birthdays and store them in database
        sync_birthdays()

        # Create events for each birthday
        event_service = GoogleEventService()
        for contact in GoogleContact.objects.all():
            print(f"Processing contact {contact}...")

            summary = (
                f"Geburtstag {contact.name} ({contact.birthday_year})"
                if contact.birthday_year
                else f"Geburtstag {contact.name}"
            )
            target_date = datetime.date(
                timezone.now().year, contact.birthday_month, contact.birthday_day
            )

            if contact.google_event_id:
                event_service.update_event(
                    event_id=contact.google_event_id,
                    summary=summary,
                    target_date=target_date,
                )
            else:
                event_id = event_service.create_event(
                    summary=summary, target_date=target_date
                )

                contact.google_event_id = event_id
                contact.save()
