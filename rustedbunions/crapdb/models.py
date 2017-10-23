from django.db import models

class Flag(models.Model):
    '''
    Database model for a flag
    '''
    flag = models.CharField(max_length=100, verbose_name="Flag")
    value = models.IntegerField(default=0, verbose_name="Flag Value")

    def __str__(self):
        return "{} = {}".format(self.flag, self.value)
