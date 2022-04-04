import django_rq
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from fees import settings as fees_settings
from fees.cron import send_subscription_reminders


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
