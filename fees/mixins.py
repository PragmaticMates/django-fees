from django.db.models import F
from django.utils.translation import ugettext_lazy as _


class PurchaserMixin(object):
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
