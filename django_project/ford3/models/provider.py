from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point, GEOSGeometry
from django.apps import apps
# from django.core.exceptions import ObjectDoesNotExist
from ford3.models.campus import Campus



class ActiveProviderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Provider(models.Model):
    PROVIDER_TYPES = (
        'TVET College',
        'University',
        'Private Tertiary College',)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,15}$',
        message=
        "Phone number must be at least 10 digits and at max 15 digits. "
        "It can start with +(country code).")
    name = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The provider's name",
        default='',
        max_length=255)
    provider_type = models.CharField(
        blank = False,
        null = False,
        unique = False,
        default='',
        help_text ="The type of the institution",
        max_length = 255)
    telephone = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The provider's switchboard",
        validators=[phone_regex],
        max_length=16)
    website = models.URLField(
        blank=True,
        null=True,
        unique=False,
        help_text="The provider's main web page",
        max_length=255)
    email = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The email address interested parties can reach you at",
        max_length=255)
    admissions_contact_no = models.CharField(
        blank=False,
        null=True,
        unique=False,
        validators=[phone_regex],
        help_text="A contact number students interested in applying can use",
        max_length=16)
    physical_address_postal_code = models.CharField(
        blank=False,
        null=False,
        unique=False,
        help_text="The provider's 4 digit post code",
        max_length=4)

    physical_address_line_1 = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="Details of the provider's physical address",
        max_length=255)
    physical_address_line_2 = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="Details of the provider's physical address",
        max_length=255)
    physical_address_city = models.CharField(
        blank=False,
        null=True,
        unique=False,
        help_text="The city which the provider is in",
        max_length=255)
    location = PointField(
        blank=True,
        null=True,
        help_text="The spatial point of the provider's head office")
    provider_logo = models.ImageField(
        blank=True,
        upload_to='provider_logo',
        help_text="The provider's logo"
    )
    postal_address_differs = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        help_text='')
    postal_address_postal_code = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='',
        max_length=4)
    postal_address_line_1 = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    postal_address_line_2 = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='',
        max_length=255)
    postal_address_city = models.CharField(
        blank=True,
        null=True,
        unique=False,
        help_text='',
        max_length=255)

    province = models.ForeignKey(
        'ford3.Province',
        null=True,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True)
    edited_at = models.DateTimeField(
        auto_now=True)

    created_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='provider_created_by'
    )

    edited_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='provider_edited_by'
    )

    deleted_by = models.ForeignKey(
        'ford3.User',
        null=True,
        on_delete=models.CASCADE,
        related_name='provider_deleted_by'
    )

    deleted = models.BooleanField(
        default=False,
        help_text='Provider has been deleted')

    objects = models.Manager()
    active_objects = ActiveProviderManager()

    def __str__(self):
        return self.name

    @property
    def campus(self):
        campus_query = Campus.active_objects.filter(
            provider__id=self.id).order_by('name')
        return list(campus_query)

    @property
    def is_new_provider(self):
        return len(self.campus) == 0

    @classmethod
    def types_to_form(self):
        return tuple(
            (provider_type, provider_type)
            for provider_type in Provider.PROVIDER_TYPES)

    def create_campus(self, campuses, created_by):
        with transaction.atomic():
            for campus_name in campuses:
                self.campus_set.create(
                    name=campus_name,
                    created_by=created_by,
                    edited_by=created_by)

    @property
    def physical_address(self):
        return f'''
            {self.physical_address_line_1},
            {self.physical_address_line_2},
            {self.physical_address_city},
            {self.physical_address_postal_code}
        '''

    @property
    def postal_address(self):
        if not self.postal_address_differs:
            return self.physical_address
        return f'''
            {self.postal_address_line_1},
            {self.postal_address_line_2},
            {self.postal_address_city},
            {self.postal_address_postal_code}
        '''

    def save(self, *args, **kwargs):
        if self.id is None:
            if len(self.name) == 0:
                raise ValidationError({'provider_name': 'Name is required.'})
        provider_name_query = Provider.objects.filter(
                name__iexact=self.name,
                deleted=False)
        provider_with_name_count = provider_name_query.count()
        # If it exists and it is not my own name raise the error

        if (provider_with_name_count > 1) or (provider_with_name_count > 0 and provider_name_query.first() != self):  # noqa
            raise ValidationError(
                {'provider_name': 'This provider\'s name is already taken.'})
        super().save(*args, **kwargs)

    def save_location_data(self, data):
        try:
            x_value = data['location_value_x']
            y_value = data['location_value_y']
            geometry_point = GEOSGeometry(Point(
                float(x_value),
                float(y_value))
            )
            self.location = geometry_point
            self.save()
        except ValueError:
            raise ValidationError(
                {
                    'location':
                        'Invalid location. Please reselect the '
                        'location from the map and ensure your location '
                        'details are entered correctly'
                 })

    def soft_delete(self):
        self.deleted = True
        for campus in self.campus_set.all():
            campus.soft_delete()
        self.save()

    @property
    def get_location_as_dict(self):
        try:
            result = ({
                'location_value_x': self.location.x,
                'location_value_y': self.location.y})
        except (IndexError, AttributeError):
            result = ({
                'location_value_x': 0,
                'location_value_y': 0})
        return result

    def import_excel_data(self, data):
        errors = {}
        for idx, obj in enumerate(data):
            errors[idx] = {}
            qualification_model = apps.get_model('ford3', 'Qualification')

            qualification_id = obj['qualification__id']
            current_qualification = qualification_model.objects.get(id=qualification_id)
            models = self.get_excel_import_models(current_qualification)
            for key in obj:
                if key == 'qualification__id':
                    continue
                key_index, key = self.parse_key(key)
                if key == 'qualification_entrance_requirement_subject__subject':
                    models['qualification_entrance_requirement_subject'], errors[idx] = (
                        self.set_qualification_entrance_rs(obj, key, key_index, current_qualification))
                elif key == 'interest__name':
                    errors[idx] = self.set_interest(obj, key, key_index, current_qualification)
                elif key == 'occupation__name':
                    errors[idx] = self.set_occupation(obj, key, key_index, current_qualification)

                else:
                    model_name = key[:key.find('__')]
                    try:
                        model = models[model_name]
                    except KeyError as e:
                        errors[idx][key] = str(e)
                    property_name = key[key.find('__')+2:]
                    property_value = obj[key]
                    if property_value and model:
                        setattr(model, property_name, property_value)
                        model.save()

    def parse_key(self, key):
        if key.find('--') != -1:  # This is a multi column insertion
            key = key[:key.find('--')]
            key_index = key[key.find('--') + 2:]
        else:
            key_index = 0
        if type(key_index) != int:
            key_index = 0
        return key_index, key

    def get_excel_import_models(self, current_qualification):
        models = {}
        models['campus'] = current_qualification.campus
        models['saqa_qualification'] = current_qualification.saqa_qualification
        models['qualification'] = current_qualification
        models['requirement'] = current_qualification.requirement

        if not models['requirement']:
            requirement = (apps.get_model('ford3', 'Requirement'))()
            requirement.qualification_id = current_qualification.id
            requirement.save()
            models['requirement'] = requirement

        return models

    def set_qualification_entrance_rs(self, excel_row_obj, key, key_index, current_qualification):
        """
        A subclass for import_excel_cell for getting the appropriate qualification_entrance_requirement_subject object
        :param obj: The excel row object being imported
        :param key: This should be qualification_entrance_requirement_subject__subject
        :param key_index: As received from parse_key(self, key)
        :param current_qualification: The qualification model object
        :return: qualification_entrance_requirement_subject to work with, errors
        """
        models_qualification_entrance_requirement_subject = None
        errors = {}
        qualification_entrance_requirement_subject_model = apps.get_model(
            'ford3', 'QualificationEntranceRequirementSubject')
        subject_model = apps.get_model('ford3', 'Subject')
        property_value = excel_row_obj[key]
        if property_value:
            try:
                excel_row_obj[key] = subject_model.objects.get(name=property_value).id
            except Exception as e:
                errors[key] = str(e)
            else:
                try:
                    models_qualification_entrance_requirement_subject = (
                        current_qualification.qualificationentrancerequirementsubject_set.all()[key_index])
                except IndexError:
                    qualification_entrance_requirement_subject = (
                        qualification_entrance_requirement_subject_model.objects.create(
                            qualification=current_qualification, subject=property_value))
                    models_qualification_entrance_requirement_subject = (
                        qualification_entrance_requirement_subject)
        return models_qualification_entrance_requirement_subject, errors

    def set_interest(self, excel_row_obj, key, key_index, current_qualification):
        """
        A subclass for import_excel_cell for adding an interest
        :param obj: The excel row object being imported
        :param key: This should be qualification_entrance_requirement_subject__subject
        :param key_index: As received from parse_key(self, key)
        :param current_qualification: The qualification model object
        :return: errors
        """
        errors = {}
        interest_model = apps.get_model('ford3', 'Interest')
        property_value = excel_row_obj[key]
        if property_value:
            try:
                interest = interest_model.objects.filter(name=property_value)[0]
            except Exception as e:  # Interest not found
                interest = interest_model.objects.create(name=property_value)
            try:
                existing_interests = list(current_qualification.interests.all().values())
                existing_interests[key_index] = interest
                current_qualification.interests.set(existing_interests)  # We overwrite the old list
            except IndexError:  # Nothing was in that slot, we add a new one
                current_qualification.interests.add(interest)
        else:
            errors[key] = 'No property value'
        return errors

    def set_occupation(self, excel_row_obj, key, key_index, current_qualification):
        """
        A subclass for import_excel_cell for adding an occupation
        :param obj: The excel row object being imported
        :param key: This should be qualification_entrance_requirement_subject__subject
        :param key_index: As received from parse_key(self, key)
        :param current_qualification: The qualification model object
        :return: errors
        """
        errors = {}
        interest_model = apps.get_model('ford3', 'Occupation')
        property_value = excel_row_obj[key]
        if property_value:
            try:
                occupation = interest_model.objects.filter(name=property_value)[0]
            except Exception as e:  # Occupation not found
                occupation = interest_model.objects.create(name=property_value)
            try:
                existing_occupations = list(current_qualification.occupations.all())
                existing_occupations[key_index] = occupation
                current_qualification.occupations.set(existing_occupations)  # We overwrite the old list
            except IndexError:  # Nothing was in that slot, we add a new one
                current_qualification.occupations.add(occupation)
        else:
            errors[key] = 'No property value'
        return errors
