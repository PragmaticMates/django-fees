from copy import deepcopy

from django.contrib import admin, messages
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

from fees.helpers import get_purchaser_model
from fees.models import Plan, Package, PackageQuota, Quota, Pricing


class PurchaserLinkMixin(object):
    def purchaser_link(self, obj):
        purchaser_model = get_purchaser_model()
        app_label = purchaser_model._meta.app_label
        model_name = purchaser_model._meta.model_name
        change_url = reverse('admin:%s_%s_change' % (app_label, model_name), args=(obj.purchaser.id,))
        return format_html('<a href="{}">{}</a>', change_url, obj.user.username)

    purchaser_link.short_description = _('Purchaser')
    purchaser_link.allow_tags = True


class QuotaInline(admin.TabularInline):
    model = PackageQuota


class PricingInline(admin.TabularInline):
    model = Pricing


class QuotaAdmin(admin.ModelAdmin):
    list_display = [
        'codename', 'name', 'description', 'unit',
        'is_boolean', 'order'
        #'move_up_down_links',
    ]
    list_display_links = ['codename']
    list_editable = ['order']


def copy_package(modeladmin, request, queryset):
    """
    Admin command for duplicating plans preserving quotas and pricings.
    """
    for package in queryset:
        package_copy = deepcopy(package)
        package_copy.id = None
        package_copy.is_available = False
        package_copy.is_default = False
        package_copy.trial_duration = 0
        package_copy.created = None
        package_copy.save(force_insert=True)

        for pricing in package.pricing_set.all():
            pricing.id = None
            pricing.plan = package_copy
            pricing.save(force_insert=True)

        for quota in package.packagequota_set.all():
            quota.id = None
            quota.package = package_copy
            quota.save(force_insert=True)


copy_package.short_description = _('Duplicate package')


class PackageAdmin(admin.ModelAdmin):
    search_fields = ('name',
                     # 'customized__username', 'customized__email',
                     )
    list_filter = ('is_available', 'is_visible')
    list_display = [
        'title',
        # 'description',
        # 'customized',
        'trial_duration',
        'is_default', 'is_available',
        'created',
        # 'move_up_down_links'
    ]
    inlines = (
        PricingInline,
        QuotaInline,
    )
    list_select_related = True
    # raw_id_fields = ('customized',)
    actions = [copy_package, ]

    # def queryset(self, request):
    #     return super(PlanAdmin, self).queryset(request).select_related(
    #         'customized'
    #     )


# class RecurringPlanInline(admin.StackedInline):
#     model = RecurringUserPlan
#     extra = 0


class PricingAdmin(admin.ModelAdmin):
    list_select_related = ['package']
    list_display = [
        'id',
        'package',
        'duration', 'period',
        'price',
        'timedelta',
    ]


class PlanAdmin(PurchaserLinkMixin, admin.ModelAdmin):
    actions = ['send_reminder']
    list_filter = (
        #'is_active',
        'expiration', 'package__title', 'package__is_available', 'package__is_visible', 'modified', 'pricing')
    search_fields = ('purchaser__email', 'package__title',)
    list_display = ('id', 'purchaser', 'package', 'pricing', 'expiration',  # 'is_active',
                    # 'recurring__automatic_renewal', 'recurring__pricing'
                    'modified')
    list_select_related = True
    readonly_fields = ['purchaser_link', ]
    # inlines = (RecurringPlanInline,)
    fields = ('purchaser', 'package', 'pricing', 'expiration', )  #'is_active')
    autocomplete_fields = ['purchaser', 'package', ]

    def recurring__automatic_renewal(self, obj):
        return obj.recurring.has_automatic_renewal
    recurring__automatic_renewal.admin_order_field = 'recurring__has_automatic_renewal'
    recurring__automatic_renewal.boolean = True

    def recurring__pricing(self, obj):
        return obj.recurring.pricing
    recurring__automatic_renewal.admin_order_field = 'recurring__pricing'

    def send_reminder(self, request, queryset):
        for obj in queryset:
            if obj.is_expired():
                messages.error(request, _('Plan %s already expired') % obj)
            else:
                messages.success(request, _('Reminder sent (%s)') % obj)
                obj.send_reminder()
    send_reminder.short_description = _('Send reminder')


admin.site.register(Quota, QuotaAdmin)
admin.site.register(Package, PackageAdmin)
# admin.site.register(Pricing, PricingAdmin)
admin.site.register(Plan, PlanAdmin)
