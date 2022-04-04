from django.urls import path
from django.utils.translation import pgettext_lazy
from fees.views import PackageListView, PlanDetailView

app_name = 'fees'

urlpatterns = [
    path(pgettext_lazy("url", 'pricing/'), PackageListView.as_view(), name='pricing'),
    path(pgettext_lazy("url", 'plan/'), PlanDetailView.as_view(), name='plan'),
]
