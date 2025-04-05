from googleapiclient.discovery import build

from birthday_sync.models import GoogleContact
from birthday_sync.services.google.authenticate import authenticate
from birthday_sync.services.google.events import GoogleEventService


def sync_birthdays():
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

    synced_contacts = []

    # Geburtstage ausgeben
    for contact in contacts:
        names = contact.get("names", [])
        birthdays = contact.get("birthdays", [])

        if names and birthdays:
            name = names[0].get("displayName", "Unbekannt")
            birthday = birthdays[0].get("date", {})
            contact_id = contact["resourceName"]

            birthday_day = birthday.get("day", None)
            birthday_month = birthday.get("month", None)
            birthday_year = birthday.get("year", None)

            if not (birthday_day and birthday_month):
                raise Exception("Missing birthday fields")

            # print(
            #     f"{name} ({contact_id}): {birthday.get('year', 'XXXX')}-{birthday.get('month', 'XX')}-"
            #     f"{birthday.get('day', 'XX')}")

            db_contact = GoogleContact.objects.filter(google_id=contact_id).first()

            if not db_contact:
                db_contact = GoogleContact(google_id=contact_id)

            db_contact.name = name
            db_contact.birthday_day = birthday_day
            db_contact.birthday_month = birthday_month
            db_contact.birthday_year = birthday_year
            db_contact.save()

            synced_contacts.append(contact_id)

    # Delete old records
    deprecated_contacts = GoogleContact.objects.exclude(google_id__in=synced_contacts)
    for dc in deprecated_contacts:
        event_service = GoogleEventService()
        event_service.delete_event(event_id=dc.google_event_id)

        dc.delete()
