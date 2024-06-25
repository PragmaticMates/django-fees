from django.apps import apps as django_apps

from fees import settings as fees_settings

VERSION = '0.2.1'


def get_package_model():
    """
    Return the Package model that is active in this project.
    """
    try:
        return django_apps.get_model(fees_settings.PACKAGE_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "FEES_PACKAGE_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "FEES_PACKAGE_MODEL refers to model '%s' that has not been installed"
            % fees_settings.PACKAGE_MODEL
        )
