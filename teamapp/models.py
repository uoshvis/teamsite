from django.db import models
from ringapp.models import Member


class Team(models.Model):

    # id = models.AutoField(primary_key=True)
    team_name = models.CharField(unique=True, max_length=100)

    # members = models.ForeignKey(Member, on_delete=models.SET_NULL,
    #                             blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name

    def get_members(self):
        return Member.objects.filter(team=self.id)
