from django.core.exceptions import ObjectDoesNotExist

from fees.models import Package


def purchaser_plan(request):
    # let's presume the purchaser is set in the request, otherwise use request.user as purchaser instance
    purchaser = getattr(request, 'purchaser', request.user)

    try:
        plan = purchaser.plan
        package = purchaser.plan.package
    except ObjectDoesNotExist:
        plan = None
        package = Package.get_default_package()

    return {
        'plan': plan,
        'package': package,
        'expiration': plan.expiration if plan else None
    }
