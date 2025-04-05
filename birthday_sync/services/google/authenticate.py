from django.conf import settings
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate() -> dict:
    creds = None

    # Token laden, falls vorhanden
    try:
        creds = Credentials.from_authorized_user_file(
            settings.BASE_DIR / "secrets/token.json", settings.GOOGLE_REQUIRED_SCOPES
        )
    except Exception:
        pass

    # Falls keine gültigen Credentials existieren, neuen OAuth-Flow starten
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            settings.BASE_DIR / "secrets/credentials.json",
            settings.GOOGLE_REQUIRED_SCOPES,
        )
        creds = flow.run_local_server(port=0)

        # Token speichern
        with open(settings.BASE_DIR / "secrets/token.json", "w") as token:
            token.write(creds.to_json())

    return creds
