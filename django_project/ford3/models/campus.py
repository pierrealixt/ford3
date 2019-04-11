from django.contrib.gis.db import models
from ford3.models.qualification import Qualification
from ford3.models.saqa_qualification import SAQAQualification
from ford3.models.campus_event import CampusEvent


class Campus(models.Model):
    provider = models.ForeignKey(
        'ford3.provider',
        on_delete=models.CASCADE)
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text='',
        max_length=255)
    location = models.PointField(
      blank=True,
      null=True,
      help_text='The spatial point position of the campus')
    photo = models.FileField(
        blank=False,
        null=True,
        help_text='Representative photo of campus',
        upload_to='campus/photo'
    )
    telephone = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    email = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    max_students_per_year = models.IntegerField(
        blank=False,
        null=True,
        unique=False,
        help_text='')
    physical_address_street_name = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)

    physical_address_city = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)

    physical_address_postal_code = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)

    postal_address_street_name = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)

    postal_address_city = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)

    postal_address_postal_code = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text='',
        max_length=255)

    pass

    @property
    def events(self):
        event_query = CampusEvent.objects.filter(
            campus__id=self.id).values(
                'date_start',
                'name',
                'http_link',
                'date_end')
        return list(event_query)

    @property
    def qualifications(self):
        qualif_query = Qualification.objects.filter(
            campus__id=self.id).order_by('id').values(
                'id',
                'saqa_qualification__name',
                'saqa_qualification__saqa_id')
        return list(qualif_query)

    @property
    def saqa_ids(self):
        return [
            str(s['saqa_qualification__saqa_id'])
            for s in self.qualifications]

    def save_form_data(self, form_data):
        for key, value in form_data.items():
            setattr(self, key, value)
        self.save()

    def save_events(self, campus_events):
        if len(campus_events) == 0:
            return
        for each_campus_event in campus_events:
            each_campus_event.campus = self
            each_campus_event.save()

    def save_qualifications(self, form_data):
        if len(form_data['saqa_ids']) == 0:
            return

        # symmetric difference
        ids = set(self.saqa_ids) ^ set(form_data['saqa_ids'].split(' '))

        for saqa_id in ids:

            saqa_qualif = SAQAQualification.objects.get(saqa_id=saqa_id)

            qualif = Qualification(
                saqa_qualification=saqa_qualif,
                campus=self)
            qualif.save()

    def delete_qualifications(self, form_data):
        # ids missing in form_data must be deleted
        ids = set(form_data['saqa_ids'].split(' ')) ^ set(self.saqa_ids)
        ids = [saqa_id for saqa_id in ids if len(saqa_id) > 0]

        for saqa_id in ids:
            qualif = Qualification.objects.filter(
                saqa_qualification__saqa_id=saqa_id)
            qualif.delete()

    def __str__(self):
        return f'{self.name} campus'
