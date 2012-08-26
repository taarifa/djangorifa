from celery.task import task
from mailer.engine import send_all

@task
def mail():
    send_all()

@task
def update_reports_status(report):
    pass

@task
def send_status_mail(issue):
    from mailer import send_mail

    # For every report associated with this issue
    for report in issue.related.related_to():
        print report
    #print report.related.related_to()
    #from django.core import mail

"""
            emails = (
                ('Hey Man', "I'm The Dude! So that's what you call me.", 'caz@glassberg-powell.com', ['cazcazn@gmail.com']),
                ('Dammit Walter', "Let's go bowlin'.", 'caz@glassberg-powell.com', ['cazcazn@gmail.com']),
            )
            results = mail.send_mass_mail(emails)
            #send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)

"""