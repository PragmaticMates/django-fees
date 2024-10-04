import django_rq
from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from fees import settings as fees_settings
from fees.cron import send_subscription_reminders

try:
    # older Django
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    # Django >= 3
    from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = 'fees'
    verbose_name = _('Fees')

    def schedule_jobs(self):
        scheduler = django_rq.get_scheduler('cron')

        if fees_settings.SCHEDULE_SUBSCRIPTION_REMINDERS:
            # Cron task to send subscription reminders
            scheduler.cron(
                "0 9 * * *",  # Run every day at 9:00 [UTC]
                # "* * * * *",  # Run every minute
                func=send_subscription_reminders,
                timeout=settings.RQ_QUEUES['cron']['DEFAULT_TIMEOUT']
            )

    def ready(self):
        from fees.models import Package

        if not fees_settings.MULTIPLE_PLANS:
            default_packages = Package.objects.filter(is_default=True)

            if default_packages.count() > 1:
                raise ImproperlyConfigured(
                    "FEES_MULTIPLE_PLANS is configured to use one default package only"
                )
