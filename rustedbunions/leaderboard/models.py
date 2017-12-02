from django.db import models

class LeaderboardEntry(models.Model):
    '''
    Database model for a leaderboard entry
    '''
    name = models.CharField(max_length=25, verbose_name="Name")
    hacker_bucks = models.IntegerField(default=0, verbose_name="Hacker Bucks")
    lifetime_hacker_bucks = models.IntegerField(default=0, verbose_name="Lifetime Hacker Bucks")
    flags_found = models.IntegerField(default=0, verbose_name="Flags found")
    playtime = models.CharField(verbose_name="Total Playtime", max_length=25)
    percent_complete = models.IntegerField(default=0, verbose_name="Percent Complete")

    def __str__(self):
        return "{} - {}".format(self.name, self.lifetime_hacker_bucks)
