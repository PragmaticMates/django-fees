from django.views.generic import ListView, DetailView

from fees.models import Package, Plan


class PackageListView(ListView):
    model = Package


class PlanDetailView(DetailView):
    model = Plan

    # TODO: get purchaser
    def get_object(self, queryset=None):
        try:
            return self.request.user.subscription
        except AttributeError:
            return None
