from django.db import models
from django.utils.timezone import now


class Member(models.Model):
    name = models.CharField(max_length=256)
    group_name = models.CharField(max_length=256)

    def __str__(self):
        return '%s of %s' % (self.name, self.group_name)


class History(models.Model):
    member = models.ForeignKey(Member, related_name="draw_histories", on_delete=models.CASCADE)
    time = models.DateTimeField(default=now)

    def __str__(self):
        return '%s at %s' % (self.member.name, self.time)