from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
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

    def save(self, *args, **kwargs):
        if self.id is None:
            if len(self.name) == 0:
                raise ValidationError({'campus': 'Name is required.'})

            if Campus.objects.filter(
                provider_id=self.provider.id,
                    name__iexact=self.name).exists():
                raise ValidationError({'campus': 'Name is already taken.'})

        super().save(*args, **kwargs)

    @property
    def events(self):
        event_query = CampusEvent.active_objects.filter(
            campus__id=self.id).order_by('id').values(
                'id',
                'name',
                'date_start',
                'date_end',
                'http_link')
        return list(event_query)

    @property
    def qualifications(self):
        return list(self.qualification_set.all().values(
            'id',
            'saqa_qualification__id',
            'saqa_qualification__name',
            'saqa_qualification__saqa_id',
            'saqa_qualification__accredited',
            'edited_at'))

    @property
    def saqa_ids(self):
        return [
            str(s['saqa_qualification__id'])
            for s in self.qualifications]

    @property
    def physical_address(self):
        if self.physical_address_line_1 is None \
            and self.physical_address_line_2 is None \
                and self.physical_address_city is None \
                and self.physical_address_postal_code is None:
            return None

        return f'''
            {self.physical_address_line_1}
            {self.physical_address_line_2}
            {self.physical_address_city}
            {self.physical_address_postal_code}
        '''

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
        if len(form_data['saqa_ids']) == 0:
            return

        # symmetric difference
        ids = set(self.saqa_ids) ^ set(form_data['saqa_ids'].split(' '))

        for saqa_id in ids:
            qualif = self.qualification_set.create()
            qualif.set_saqa_qualification(saqa_id)
            qualif.save()

    def delete_qualifications(self, form_data):
        # ids missing in form_data must be deleted
        ids = set(form_data['saqa_ids'].split(' ')) ^ set(self.saqa_ids)
        ids = [saqa_id for saqa_id in ids if len(saqa_id) > 0]

        for saqa_id in ids:
            qualif = self.qualification_set.filter(
                saqa_qualification__id=saqa_id,
                campus=self)
            qualif.delete()

    def __str__(self):
        return self.name
