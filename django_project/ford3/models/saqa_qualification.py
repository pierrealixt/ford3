from django.db import models
from ford3.models.sub_field_of_study import SubFieldOfStudy
from ford3.models.field_of_study import FieldOfStudy
from django.core.exceptions import ValidationError


class SAQAQualification(models.Model):
    field_of_study = models.ForeignKey(
        FieldOfStudy,
        null=True,
        blank=True,
        on_delete=models.PROTECT)

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
        null=True,
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
        if self.creator_provider:
            creator_provider_id = self.creator_provider.id
        else:
            creator_provider_id = None

        return {
            'id': self.id,
            'saqa_id': self.saqa_id,
            'name': self.name,
            'accredited': self.accredited,
            'creator_provider_id': creator_provider_id
        }

    @classmethod
    def create_non_accredited(self, name, creator_provider):
        saqa_qualif = SAQAQualification(
            name=name,
            creator_provider=creator_provider,
            accredited=False,
            saqa_id=0)

        saqa_qualif.save()

        return saqa_qualif

    @classmethod
    def create_accredited(self, name, saqa_id):
        saqa_qualif = SAQAQualification(
            name=name,
            saqa_id=saqa_id)

        saqa_qualif.save()

        return saqa_qualif

    @classmethod
    def get_or_create_accredited(self, saqa_dict):
        try:
            return SAQAQualification.objects.get(saqa_id=saqa_dict['saqa_id'])
        except SAQAQualification.DoesNotExist:
            return self.create_accredited(
                saqa_dict['name'],
                saqa_dict['saqa_id'])

    def save(self, *args, **kwargs):
        if len(self.name) == 0:
            raise ValidationError({'saqa_qualification': 'Name is required.'})

        if self.accredited:
            # make sure saqa_id and name are unique
            pass
        else:
            # make sure creator_provider and name are unique
            if SAQAQualification.objects.filter(
                creator_provider=self.creator_provider,
                    name=self.name).exists():
                raise ValidationError(
                    {'saqa_qualification': 'Non-accredited SAQA qualification \
                    name must be unique per provider.'})

        super().save(*args, **kwargs)

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
