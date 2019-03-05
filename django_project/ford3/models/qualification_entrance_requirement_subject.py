from django.db import models
from ford3.models.qualification import Qualification
from ford3.models.subject import Subject


class QualificationEntranceRequirementSubject(models.Model):
    qualification_id = models.ForeignKey(
        Qualification,
        on_delete=models.PROTECT)
    subject_id = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT)

    id = models.IntegerField(
        blank=False,
        null=False,
        unique=True,
        help_text='',
        primary_key=True)
    minimum_score = models.IntegerField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
    required = models.BooleanField(
        blank=False,
        null=False,
        unique=False,
        help_text='')
