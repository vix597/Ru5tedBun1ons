from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, verbose_name="Username")
    password = models.CharField(max_length=100, verbose_name="password")
    security_question = models.CharField(max_length=1000, verbose_name="Security Question")
    security_answer = models.CharField(max_length=100, verbose_name="Security Answer")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.username)
