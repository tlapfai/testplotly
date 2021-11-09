from django.db import models

class IRCurve(models.Model):
    pass

class EuropeanOption(models.Model):
    local_curve = models.ForeignKey("IRCurve", on_delete=models.DO_NOTHING, related_name="options_as_r")
    foreign_curve = models.ForeignKey("IRCurve", on_delete=models.DO_NOTHING, related_name="options_as_q")
    content = models.TextField(null=True)
