from django.views.generic import ListView, DetailView

from fees.models import Package, Plan, Pricing


class PackageListView(ListView):
    model = Package

    def get_queryset(self):
        return super().get_queryset().visible()

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data.update({'distinct_period_durations': Pricing.distinct_period_durations()})
        return context_data


class PlanDetailView(DetailView):
    model = Plan

    # TODO: get purchaser
    def get_object(self, queryset=None):
        try:
            return self.request.user.subscription
        except AttributeError:
            return None
