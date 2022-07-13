from django.db.models import F
from django.utils.translation import ugettext_lazy as _


class PurchaserMixin(object):
    @property
    def plan(self):
        return self.plan_history\
            .active()\
            .order_by(
                F('expiration').desc(nulls_last=True)
            ).first()

    @plan.setter
    def plan(self, plan):
        if plan.purchaser and plan.purchaser != self:
            raise ValueError(_('Purchaser already set in the plan: %s') % plan.purchaser)
        plan.purchaser = self
        plan.save()

    @property
    def plan_history(self):
        return self.plan_set.all()
