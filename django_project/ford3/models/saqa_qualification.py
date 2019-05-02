from django.db import models
from ford3.models.sub_field_of_study import SubFieldOfStudy


class SAQAQualification(models.Model):
    sub_field_of_study = models.ForeignKey(
        SubFieldOfStudy,
        null=True,
        blank=True,
        on_delete=models.PROTECT)
    saqa_id = models.IntegerField(
        blank=False,
        null=False,
        help_text="The ID of the qualification as listed in the SAQA database")
    name = models.CharField(
        blank=False,
        null=False,
        help_text="The name of the qualification as approved by SAQA",
        max_length=255)
    nqf_level = models.IntegerField(
        blank=True,
        null=True,
        help_text="The NQF level SAQA has attributed to this qualification")
    creator_provider = models.ForeignKey(
        'ford3.provider',
        null=True,
        blank=True,
        on_delete=models.CASCADE)
    accredited = models.BooleanField(
        default=True,
        blank=False,
        null=False)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'saqa_id': self.saqa_id,
            'name': self.name
        }

    def search(query):
        try:
            query = int(query)
            results = SAQAQualification.objects.filter(
                saqa_id=query)
        except ValueError:
            # query is not an integer
            results = SAQAQualification.objects.filter(
                name__icontains=query)

        results = [obj.as_dict() for obj in results]

        return results
