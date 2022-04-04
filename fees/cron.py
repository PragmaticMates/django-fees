def send_subscription_reminders():
    from fees import jobs
    jobs.send_subscription_reminders.delay(7)
    jobs.send_subscription_reminders.delay(1)
