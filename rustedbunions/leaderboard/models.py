from django.db import models
from django.utils import timezone

from core.util import ObjectId

class LeaderboardEntry(models.Model):
    '''
    Database model for a leaderboard entry
    '''
    name = models.CharField(max_length=25, verbose_name="Name")
    display_name = models.CharField(default="", max_length=25, verbose_name="Display Name")
    hacker_bucks = models.IntegerField(default=0, verbose_name="Hacker Bucks")
    lifetime_hacker_bucks = models.IntegerField(default=0, verbose_name="Lifetime Hacker Bucks")
    num_flags_found = models.IntegerField(default=0, verbose_name="Number of Flags Found")
    claimed_flags = models.CharField(default="", max_length=4000, verbose_name="List of Claimed Flags")
    playtime = models.CharField(verbose_name="Total Playtime", max_length=25)
    percent_complete = models.IntegerField(default=0, verbose_name="Percent Complete")
    secret_key = models.CharField(default="", max_length=128, verbose_name="Secret Key")
    leader_oid = models.CharField(default=ObjectId(), max_length=32, verbose_name="Leader OID")
    session_creation_time = models.DateTimeField(default=timezone.now, verbose_name="Session Creation Time")
    purchased_challenges = models.CharField(default="", max_length=4000, verbose_name="Purchased Challenges")
    remote_ip = models.CharField(default="", max_length=64, verbose_name="Remote IP")
    last_modified = models.DateTimeField(auto_now=True)
    leader_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.lifetime_hacker_bucks)
