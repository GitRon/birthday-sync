import io
import sys

from django.core.management import BaseCommand
from googleapiclient.discovery import build

from services.google.authenticate import authenticate


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Authenticate at Google
        creds = authenticate()

        # Google People API aufrufen
        service = build("people", "v1", credentials=creds)
        results = (
            service.people()
            .connections()
            .list(
                resourceName="people/me",
                pageSize=1000,
                personFields="birthdays,names,metadata",
            )
            .execute()
        )

        contacts = results.get("connections", [])

        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

        for contact in contacts:
            names = contact.get("names", [])
            birthdays = contact.get("birthdays", [])

            if names and not birthdays:
                print(names[0].get("displayName", "Unbekannt"))
