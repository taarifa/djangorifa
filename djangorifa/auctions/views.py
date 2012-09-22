from olwidget.widgets import Map, InfoLayer
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from facilities.models import Facility, FacilityIssue
from auctions.filtersets import FacilityFilterSet
from django.utils.encoding import force_unicode
from taarifa_config.models import TaarifaConfig
from django.shortcuts import render
from functools import wraps

def access_denied(request):
    return render(request, "auctions/access_denied.html")

''' Determines whether or not someone is a worker, and is therefore able to make bids '''
def is_worker(user):
    if user: return user.groups.filter(name="Worker").count()
    return False

def is_creator(view_func):
    def decorator(request, *args, **kwargs):
        # The only argument is the first one, which is the user's id
        # If they match, return the view
        # Thanks to URL regex, this will always be fine
        if request.user.pk == int(args[0]):
            return view_func(request, *args, **kwargs)
        # Otherwise redirect to the denied page
        return access_denied(request)
    return decorator

# @is_creator
def view_jobs(request, user_id):
    return render(request, "auctions/user_jobs.html")

# @user_passes_test(is_worker, login_url="auctions/access_denied.html")
def view_auction(request):
    config = TaarifaConfig.objects.get_current()

    # If the auctions is currently not in use, return a 404
    # if not config.use_auction: raise Http404

    # Determine which module to import, according to the auction type
    try: auction_type = config.auctionconfig.auction_type
    except: auction_type = "open"
    import_string = "auctions.%s.views" % auction_type

    # If there is a post thingy happening, process with the correct auction type
    if request.method == "POST":
        # Import the module with bid function
        module = __import__(import_string, fromlist=['bid'])
        make_bid = getattr(module, 'bid')
        make_bid(request)

    # Populate the information common to all auctions
    facility = request.GET.get('facility', None)
    num_pages = request.GET.get('num', 25) # Default to 25 per page

    filterset = FacilityFilterSet(request.GET or None, queryset=FacilityIssue.objects.select_related(depth=1).all())

    # Create the paginator with the query
    paginator = Paginator(filterset.qs, num_pages)
    page = request.GET.get('page')
    try: fac_issues = paginator.page(page)

    # If page is not an integer, deliver first page.
    except PageNotAnInteger: fac_issues = paginator.page(1)

    # If page is out of range (e.g. 9999), deliver last page of results.
    except EmptyPage: fac_issues = paginator.page(paginator.num_pages)

    # Evaluate the query set and generate the information for the map widget
    issues = [[f.facility.location, "Facility: %d" % f.pk] for f in filterset.qs]

    # If the query set is empty, either there are no issues, or there are no facilities!
    if not issues:
        if Facility.objects.count() > 0:
            if facility:
                fac = Facility.objects.get(pk=facility)
                issues = [[fac.location, force_unicode(fac)],]

    # Create a map to display
    lon, lat = config.get_center().coords
    issue_map = Map([
        InfoLayer(issues, {
            'name':'facilities',
            'cluster':True,
            'overlay_style': {
                'fill_color':"${specialAttributeHandler}",
            },
            'overlay_style_context': {
                'specialAttributeHandler': 'function(feature) {}',
            },
        })
    ], {
        'overlay_style': {
            'fill_opacity': 0.1,
            'fill_color':'#ffa500',
            'stroke_color':'#ffa500'
        },
        'default_lat': lat,
        'default_lon': lon,
        'default_zoom':17,
        'map_div_style': {
            'width':'100%',
            'height':'100%'
        }
    })

    # Determine the correct view function to return and return it
    module = __import__(import_string, fromlist=['view'])
    view_issues = getattr(module, 'view')
    return view_issues(request, fac_issues, filterset, issue_map)
