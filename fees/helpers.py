from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

from fees import settings as fees_settings


def get_purchaser_model():
    """
    Return the model that represents purchaser object.
    """
    try:
        return django_apps.get_model(fees_settings.PURCHASER_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured("FEES_PURCHASER_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "FEES_PURCHASER_MODEL refers to model '%s' that has not been installed" % fees_settings.PURCHASER_MODEL
        )
