from django.db import models
from django.contrib.gis.db.models import PointField


class Consumer(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    street = models.CharField(max_length=20)
    status = models.CharField(max_length=12)
    previous_jobs_count = models.IntegerField()
    amount_due = models.IntegerField()
    location = PointField()

    def __str__(self):
        return f"{self.street}"
