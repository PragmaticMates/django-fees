from django_rq import job


@job('default')
def send_subscription_reminders(threshold):
    from fees.models import Plan

    expiring_plans = Plan.objects.expires_in(days=threshold)
    total_plans = expiring_plans.count()
    print(f'Found {total_plans} expiring plans in {threshold} days')

    for plan in expiring_plans:
        print(plan, plan.pricing, plan.expiration)
        plan.send_reminder()
