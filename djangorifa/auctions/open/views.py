from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from facilities.models import FacilityIssue

# Theoretically, this decorator should always return true as the only way this view is reached is through another
# Performing another check to see if worker is a bit excessive.
@login_required
def view(request, fac_issues, filterset, issue_map):
    if request.method == "POST":
        print 'kk'
    return render(request, "auctions/open/view.html", {'fac_issues': fac_issues, 'filterset': filterset, 'map': issue_map})

# As this is called after a post, it will return a redirect
@login_required
def bid(request):
    from django.http import HttpResponseRedirect
    from django.contrib import messages

    # Get the bid from the request
    for value in request.POST.keys():
        if not value == "csrfmiddlewaretoken":
            issue_id = int(value.replace('name-bid-', ''))

    # Check to see there isn't a lock on the facility issue
    # One fell swoop on the update to prevent race conditions
    if(FacilityIssue.objects.filter(pk=issue_id, locked=False).update(locked=True)):
        issue = FacilityIssue.objects.filter(pk=issue_id)
        if issue.count() > 0:
            issue = issue[0]
            # Create a bid for this object
            from auctions.models import Bid
            Bid(user=request.user, amount=issue.cost, issue=issue).save()
            messages.add_message(request, messages.WARNING, "Your bid was successful! Please start work ASAP!")

    # If everything hasn't gone to plan, add a message telling the user that's the case
    else: messages.add_message(request, messages.WARNING, "Your bid was unsuccessful! Please try again.")

    return HttpResponseRedirect("/jobs/")
