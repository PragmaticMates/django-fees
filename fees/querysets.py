from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class PackageQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(is_visible=True)


class PlanQuerySet(models.QuerySet):
    def expires_in(self, days=7):
        threshold = now() + timedelta(days=days)
        return self.filter(expiration=threshold.date())
