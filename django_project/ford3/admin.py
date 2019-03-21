from django.contrib import admin # noqa
from ford3.models import (
    Campus,
    Qualification,
    QualificationEntranceRequirementSubject,
    Provider,
    Requirement,
    Subject,
    SecondaryInstitutionType
)

# Register your models here.
admin.site.register(Campus)
admin.site.register(Provider)
admin.site.register(Qualification)
admin.site.register(QualificationEntranceRequirementSubject)
admin.site.register(Requirement)
admin.site.register(Subject)
admin.site.register(SecondaryInstitutionType)
