STATUS_CHOICES = ((1, 'Awaiting Verification'), (2, 'Unassigned'), (3, 'Assigned'), (4, 'Fixed'), (5, 'Dispute Resolution'))

def get_reported_issues():
    from reports.models import ReportedIssue

    # Need to create a stack to give recursiveness
    # Obviously generators don't work with recursion
    klass = ReportedIssue
    stack = []

    while stack or klass:
        for issue in klass.__subclasses__():
            if issue._meta.abstract:
                stack.append(issue)
            else:
                yield issue
                klass = None

        if stack: klass = stack.pop()
