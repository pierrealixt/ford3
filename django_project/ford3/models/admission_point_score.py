from django.db import models
from ford3.models.people_group import PeopleGroup


class AdmissionPointScore(models.Model):
    requirement = models.ForeignKey(
        'ford3.Requirement',
        on_delete=models.CASCADE)

    people_group = models.ForeignKey(
        'ford3.PeopleGroup',
        on_delete=models.CASCADE)

    value = models.IntegerField(
        blank=True,
        null=True,
        help_text="The admission point score required for the qualification")

    @staticmethod
    def init():
        return [
            {
                'id': 0,
                'value': 0,
                'group': {'id': pg.id, 'name': pg.group}
            }
            for pg in PeopleGroup.objects.all()
        ]
