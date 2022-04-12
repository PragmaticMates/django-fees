from django.views.generic import ListView, DetailView

from fees.models import Package, Plan


class PackageListView(ListView):
    model = Package

    def get_queryset(self):
        return super().get_queryset().visible()


class PlanDetailView(DetailView):
    model = Plan

    # TODO: get purchaser
    def get_object(self, queryset=None):
        try:
            return self.request.user.subscription
        except AttributeError:
            return None
