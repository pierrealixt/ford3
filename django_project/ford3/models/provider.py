from django.core.validators import RegexValidator
from django.db import models, transaction
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
