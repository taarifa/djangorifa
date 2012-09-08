from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from facilities.forms import FacilityReportForm
from facilities.models import Facility

@permission_required('reports.can_add')
def new_report(request, pk):
    template = "facilities/report.html"
    if request.method == "POST":
        form = FacilityReportForm(pk, request.POST)
        if form.is_valid():
            saved = form.save(request)
            return HttpResponseRedirect('/reports/ajax/reported/%d' % saved.pk)
    else:
        form = FacilityReportForm(Facility.objects.get(pk=pk).pk)
        if not form.has_reportables:
            from mailer import mail_admins
            mail_admins("Facility not reportable: %s" % reverse('admin:facilities_facility_change', args=[pk]),
                "Please add some reportable items to rectify the situation.")
            return render(request, "facilities/not_reportable.html")
    return render(request, template, {'form':form})


def view_report(request, pk):
    return HttpResponse('moo')
