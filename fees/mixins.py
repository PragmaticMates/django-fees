import datetime
from django.db.models import F

try:
    # older Django
    from django.utils.translation import ugettext_lazy as _
except ImportError:
    # Django >= 3
    from django.utils.translation import gettext_lazy as _


class PurchaserMixin(object):
    created_attribute = 'created'

    def is_package_quota_available(self, quota):
        package = self.package
        return quota in package.get_quotas() if package is not None else False

    @property
    def package(self):
        from fees.models import Package
        return Package.get_current_package(self)

    @property
    def plan(self):
        return self.plan_history\
            .active()\
            .order_by(
                '-modified',
                # F('expiration').desc(nulls_last=True)
            ).first()

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
        if not self.package or not self.plan:
            return False

        trial_duration = self.package.trial_duration

        if not trial_duration or trial_duration <= 0:
            return False

        created_date = getattr(self, self.created_attribute, None)
        plan_expiration_date = self.plan.expiration

        if created_date is not None and plan_expiration_date is not None:
            created_date = created_date.date() if isinstance(created_date, datetime.datetime) else created_date
            delta = plan_expiration_date - created_date

            if delta.days <= trial_duration:
                return True

        return False
