from django import template

from fees.models import Quota, Package

register = template.Library()


@register.simple_tag
def package_quotas_info(package):
    quotas = Quota.objects.values('codename', 'name_i18n', 'description_i18n', 'is_boolean')
    all_quotas = dict((
        q['codename'],
        {
            'name': q['name_i18n'],
            'description': q['description_i18n'],
            'is_boolean': q['is_boolean'],
        }
    ) for q in quotas)

    quotas_info = all_quotas.copy()
    package_quotas = package.packagequota_set.all().values('quota__codename', 'value')

    for package_quota in package_quotas:
        codename = package_quota['quota__codename']
        quota = quotas_info[codename]

        quota.update({'is_available': Package.is_quota_available(package_quota)})

        if not quota['is_boolean']:
            quota.update({
                'value': package_quota['value'],
            })

    return quotas_info
