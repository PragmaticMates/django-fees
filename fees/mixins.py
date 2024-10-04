import datetime
from django.core.exceptions import ImproperlyConfigured

try:
    # older Django
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    # Django >= 3
    from django.utils.translation import gettext_lazy as _

from fees import get_package_model
from fees import settings as fees_settings


class PurchaserMixin(object):
    created_attribute = 'created'

    def is_package_quota_available(self, quota):
        return quota in self.quotas

    @property
    def quotas(self):
        if fees_settings.MULTIPLE_PLANS:
            quotas = {}

            for package in self.packages:
                quotas.update(package.get_quotas())

            return quotas
        else:
            package = self.package
            return package.get_quotas() if package is not None else {}


    @property
    def package(self):
        if fees_settings.MULTIPLE_PLANS:
            raise ImproperlyConfigured(
                "FEES_MULTIPLE_PLANS is configured to use single package"
            )
        return get_package_model().get_current_package(self)

    @property
    def packages(self):
        if not fees_settings.MULTIPLE_PLANS:
            raise ImproperlyConfigured(
                "FEES_MULTIPLE_PLANS is configured to use multiple packages"
            )
        return get_package_model().get_current_packages(self)

    @property
    def plan(self):
        if fees_settings.MULTIPLE_PLANS:
            raise ImproperlyConfigured(
                "FEES_MULTIPLE_PLANS is configured to use multiple plans"
            )

        return self.plan_history\
            .active()\
            .order_by(
                '-modified',
                # F('expiration').desc(nulls_last=True)
            ).first()

    @property
    def plans(self):
        if not fees_settings.MULTIPLE_PLANS:
            raise ImproperlyConfigured(
                "FEES_MULTIPLE_PLANS is configured to use single plan only"
            )

        return self.plan_history \
            .active() \
            .order_by(
            '-modified',
        )

    @plan.setter
    def plan(self, plan):
        if plan.purchaser and plan.purchaser != self:
            raise ValueError(_('Purchaser of the plan is already set: %s') % plan.purchaser)
        plan.purchaser = self
        plan.save()

    @property
    def plan_history(self):
        return self.plan_set.all()

    @property
    def is_in_free_trial(self):
        trial_duration = None
        plan_expiration_date = None

        if fees_settings.MULTIPLE_PLANS:
            if not self.packages or not self.plans.exists():
                return False

            for plan in self.plans:
                if plan.package.trial_duration:
                    trial_duration = plan.package.trial_duration
                    plan_expiration_date = plan.expiration
                    break

        else:
            if not self.package or not self.plan:
                return False

            trial_duration = self.package.trial_duration
            plan_expiration_date = self.plan.expiration

        if not trial_duration or trial_duration <= 0:
            return False

        created_date = getattr(self, self.created_attribute, None)

        if created_date is not None and plan_expiration_date is not None:
            created_date = created_date.date() if isinstance(created_date, datetime.datetime) else created_date
            delta = plan_expiration_date - created_date

            if delta.days <= trial_duration:
                return True

        return False
