from django.db.models import F


class PurchaserMixin(object):
    @property
    def plan(self):
        ordered_plan_history = self.plan_history.active().order_by(F('expiration').desc(nulls_last=True))
        plan = ordered_plan_history.first()
        return plan

    @plan.setter
    def plan(self, plan):
        plan.purchaser = self
        plan.save()

    @property
    def plan_history(self):
        return self.plan_set.all()
