from django.db import models


class AirportRoute(models.Model):
    airport_code = models.CharField(max_length=10, unique=True)
    position = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(
        help_text="Duration to the next airport in minutes"
    )
    next_airport = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.airport_code} -> {self.next_airport}"