from django.conf import settings

PURCHASER_MODEL = getattr(settings, 'FEES_PURCHASER_MODEL', settings.AUTH_USER_MODEL)
CURRENCY = getattr(settings, 'FEES_CURRENCY', 'EUR')
SCHEDULE_SUBSCRIPTION_REMINDERS = getattr(settings, 'FEES_SCHEDULE_SUBSCRIPTION_REMINDERS', False)
