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
        help_text='The name of the campus',
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
        help_text="The campus' telephone number",
        max_length=255)
    email = models.EmailField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' email",
        max_length=255)
    max_students_per_year = models.PositiveIntegerField(
        blank=False,
        null=True,
        unique=False,
        help_text="Maximum number of students")
    physical_address_line_1 = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' physical address details",
        max_length=255)
    physical_address_line_2 = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' physical address details",
        max_length=255)

    physical_address_city = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' physical address city",
        max_length=255)

    physical_address_postal_code = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' physical address postal code",
        max_length=255)

    postal_address_differs = models.BooleanField(
        blank=False,
        null=True,
        default=False,
        help_text="Is the postal address different from the physical address?")

    postal_address_line_1 = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' postal address",
        max_length=255)

    postal_address_line_2 = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' postal address",
        max_length=255)

    postal_address_city = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' postal address city",
        max_length=255)

    postal_address_postal_code = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The campus' postal adress code",
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
                'saqa_qualification__id',
                'saqa_qualification__name',
                'saqa_qualification__saqa_id',
                'saqa_qualification__accredited')
        return list(qualif_query)

    @property
    def saqa_ids(self):
        return [
            str(s['saqa_qualification__id'])
            for s in self.qualifications]

    def save_postal_data(self, form_data):
        postal_address_differs = form_data.get(
            'postal_address_differs', '')
        physical_address_line_1 = form_data.get(
                'physical_address_line_1', '')
        physical_address_line_2 = form_data.get(
            'physical_address_line_2', '')
        physical_address_city = form_data.get(
            'physical_address_city', '')
        physical_address_postal_code = form_data.get(
            'physical_address_postal_code', '')
        if not postal_address_differs:
            postal_address_line_1 = physical_address_line_1
            postal_address_line_2 = physical_address_line_2
            postal_address_city = physical_address_city
            postal_address_postal_code = physical_address_postal_code
        else:
            postal_address_line_1 = form_data.get(
                'postal_address_line_1', '')
            postal_address_line_2 = form_data.get(
                'postal_address_line_2', '')
            postal_address_city = form_data.get(
                'postal_address_city', '')
            postal_address_postal_code = form_data.get(
                'postal_address_postal_code', '')
        setattr(self,
                'physical_address_line_1', physical_address_line_1)
        setattr(self,
                'physical_address_line_2', physical_address_line_2)
        setattr(self,
                'physical_address_city', physical_address_city)
        setattr(self,
                'physical_address_postal_code', physical_address_postal_code)
        setattr(self,
                'postal_address_line_1', postal_address_line_1)
        setattr(self,
                'postal_address_line_2', postal_address_line_2)
        setattr(self,
                'postal_address_city', postal_address_city)
        setattr(self,
                'postal_address_postal_code', postal_address_postal_code)
        setattr(self,
                'postal_address_differs', postal_address_differs)
        self.save()

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
        print(form_data['saqa_ids'])
        if len(form_data['saqa_ids']) == 0:
            return

        # symmetric difference
        ids = set(self.saqa_ids) ^ set(form_data['saqa_ids'].split(' '))

        for saqa_id in ids:

            saqa_qualif = SAQAQualification.objects.get(id=saqa_id)

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
                saqa_qualification__id=saqa_id,
                campus=self)
            qualif.delete()

    def save_event(self, form_data):
        i = 0

    def __str__(self):
        return self.name
