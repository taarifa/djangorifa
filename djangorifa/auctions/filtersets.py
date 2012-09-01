import django_filters
from facilities.models import FacilityIssue
from auctions.forms import AuctionFilterForm

class FacilityFilterSet(django_filters.FilterSet):

    class Meta:
        model = FacilityIssue
        form = AuctionFilterForm
        fields = ['facility',]
        order_by = ['facility', 'cost', 'content_type']
