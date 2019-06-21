from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point, GEOSGeometry
from ford3.models.campus_event import CampusEvent
from ford3.completion_audit.rules import CAMPUS as completion_rules


class ActiveCampusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


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
        help_text="The campus' switchboard",
        max_length=16)
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
        help_text="The campus' physical address post code",
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

    created_at = models.DateTimeField(
        auto_now_add=True)
    edited_at = models.DateTimeField(
        auto_now=True)

    created_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='campus_created_by'
    )

    edited_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='campus_edited_by'
    )

    deleted_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='campus_deleted_by'
    )

    deleted = models.BooleanField(
        default=False,
        help_text="Campus has been deleted")
    
    completion_rate = models.PositiveIntegerField(
        blank=True,
        null=True,
        default=0,
        help_text="How much of the campus' details has been completed?"
    )

    COMPLETION_RULES = completion_rules


    objects = models.Manager()
    active_objects = ActiveCampusManager()

    def save(self, *args, **kwargs):
        if self.id is None:
            if len(self.name) == 0:
                raise ValidationError({'campus': 'Name is required.'})

            if Campus.objects.filter(
                provider_id=self.provider.id,
                    name__iexact=self.name,
                    deleted=False).exists():
                raise ValidationError({'campus': 'Name is already taken.'})
        super().save(*args, **kwargs)

    def save_location_data(self, cleaned_data):
        x_value = cleaned_data['location_value_x']
        y_value = cleaned_data['location_value_y']
        geometry_point = GEOSGeometry(Point(
            x_value,
            y_value))
        self.location = geometry_point

        self.save()

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
        queryset = self.qualification_set \
            .filter(deleted=False) \
            .values(
                'id',
                'saqa_qualification__id',
                'saqa_qualification__name',
                'saqa_qualification__saqa_id',
                'saqa_qualification__accredited',
                'edited_at',
                'published',
                'ready_to_publish',
                'completion_rate')
        return list(queryset)

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

    @property
    def postal_address(self):
        if self.postal_address_line_1 is None \
            and self.postal_address_line_2 is None \
                and self.postal_address_city is None \
                and self.postal_address_postal_code is None:
            return None

        return f'''
            {self.postal_address_line_1}
            {self.postal_address_line_2}
            {self.postal_address_city}
            {self.postal_address_postal_code}
        '''
    
    @property
    def qualifications_completion_rate(self):
        try:
            return int(sum([
                qualification['completion_rate']
                for qualification in self.qualifications
            ]) / len(self.qualifications))
        except ZeroDivisionError:
            return 0

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

    def save_qualifications(self, form_data, created_by):
        if len(form_data['saqa_ids']) == 0:
            return

        # symmetric difference
        ids = set(self.saqa_ids) ^ set(form_data['saqa_ids'].split(' '))

        for saqa_id in ids:
            qualif = self.qualification_set.create(
                created_by=created_by,
                edited_by=created_by
            )
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
