from django import forms
from django.contrib import admin # noqa
from ford3.models import (
    Campus,
    CampusEvent,
    Qualification,
    QualificationEntranceRequirementSubject,
    Provider,
    Requirement,
    Interest,
    Occupation,
    Subject,
    SecondaryInstitutionType,
    QualificationEvent,
    SAQAQualification,
    Prospect,
    User
)


# bypass provider form validation in the Django Administration
class ProviderAdminForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name']


class ProviderAdmin(admin.ModelAdmin):
    form = ProviderAdminForm


admin.site.register(Provider, ProviderAdmin)


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'is_staff',
            'is_province',
            'is_provider',
            'is_campus']


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm


admin.site.register(User, UserAdmin)


admin.site.register(Campus)
admin.site.register(CampusEvent)
admin.site.register(Qualification)
admin.site.register(QualificationEntranceRequirementSubject)
admin.site.register(Requirement)
admin.site.register(Interest)
admin.site.register(Occupation)
admin.site.register(Subject)
admin.site.register(SecondaryInstitutionType)
admin.site.register(QualificationEvent)
admin.site.register(SAQAQualification)
admin.site.register(Prospect)
