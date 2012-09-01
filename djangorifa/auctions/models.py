from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from facilities.models import FacilityIssue
from taarifa_config.models import TaarifaConfig

from reports.models import ReportedIssue

# Defines the fields needed to keep track of bids
class Bid(models.Model):
    user = models.ForeignKey(User)
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    issue_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    issue = generic.GenericForeignKey("issue_type", "object_id")
    #issue = models.ForeignKey(FacilityIssue)

    # If a bid is being created, the issue needs to be set to the correct status
    def save(self, *args, **kwargs):
        # It's a new model
        if not self.pk:
            # Get content type of
            self.issue.status = 3
            self.issue.save()
        super(Bid, self).save(*args, **kwargs)

def generate_auction_choices():
    import auctions, pkgutil
    choices = []
    for _, modname, ispkg in pkgutil.iter_modules(auctions.__path__):
        if ispkg: choices.append([modname,modname.title()])
    return choices

# Extend the TaarifaConfig with auction-specific stuff
class AuctionConfig(models.Model):
    AUCTION_CHOICES = generate_auction_choices()
    auction_type = models.CharField(max_length=30, choices=AUCTION_CHOICES)
    #use_auction = models.BooleanField()

    # Add a one-to-one field for enabling different configs
    config = models.OneToOneField(TaarifaConfig)
    #urgent_time = models.PositiveIntegerField()
    #non_urgent_time = models.PositiveIntegerField()

    class Meta:
        verbose_name = verbose_name_plural = "Configure Auction Settings"
