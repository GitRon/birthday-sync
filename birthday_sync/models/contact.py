from django.db import models


class GoogleContact(models.Model):
    google_id = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=255)
    birthday_day = models.PositiveSmallIntegerField()
    birthday_month = models.PositiveSmallIntegerField()
    birthday_year = models.PositiveSmallIntegerField(null=True, blank=True)
    google_event_id = models.CharField(
        unique=True, max_length=100, blank=True, null=True
    )

    def __str__(self):
        return self.name
