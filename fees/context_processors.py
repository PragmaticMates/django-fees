from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured

from fees.models import Package
from fees import settings as fees_settings

def purchaser_plan(request):
    if fees_settings.MULTIPLE_PLANS:
        raise ImproperlyConfigured(
            "FEES_MULTIPLE_PLANS is configured to use multiple purchaser plans"
        )

    # let's presume the purchaser is set in the request, otherwise use request.user as purchaser instance
    purchaser = getattr(request, 'purchaser', request.user)

    try:
        plan = purchaser.plan
        package = purchaser.plan.package
    except (ObjectDoesNotExist, AttributeError):
        plan = None
        package = Package.get_fallback_package()

    return {
        'plan': plan,
        'package': package,
        'expiration': plan.expiration if plan else None
    }


def purchaser_plans(request):
    if not fees_settings.MULTIPLE_PLANS:
        raise ImproperlyConfigured(
            "FEES_MULTIPLE_PLANS is configured to use single purchaser plan"
        )

    # let's presume the purchaser is set in the request, otherwise use request.user as purchaser instance
    purchaser = getattr(request, 'purchaser', request.user)

    try:
        plans = purchaser.plans
        packages = [plan.package for plan in purchaser.plans]

    except (ObjectDoesNotExist, AttributeError):
        plans = None
        packages = [Package.get_fallback_package()]

    return {
        'plans': plans,
        'packages': packages,
        'expirations': [plan.expiration for plan in plans]
    }
