from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils.timezone import now


class PackageQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(is_visible=True)


class PlanQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            Q(activation__lte=now()),
            Q(expiration=None) | Q(expiration__gte=now()),
        )

    def expires_in(self, days=7):
        threshold = now() + timedelta(days=days)
        return self.filter(expiration=threshold.date())
