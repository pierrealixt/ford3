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
    User,
    ProvinceUser,
    Province
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
            'is_superuser']


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm



class ProvinceAdminForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = ['name']


class ProvinceAdmin(admin.ModelAdmin):
    form = ProvinceAdminForm


admin.site.register(Province, ProvinceAdmin)
class ProvinceUserAdminForm(forms.ModelForm):
    class Meta:
        model = ProvinceUser
        fields = [
            'email', 'provinces'
        ]

class ProvinceUserAdmin(admin.ModelAdmin):
    form = ProvinceUserAdminForm
    list_display = ('email', 'get_provinces')

    def get_provinces(self, obj):
        # todo it should call a model method
        # e.g: get_provinces_for_admin
        return "\n".join([p.name for p in obj.provinces.all()])

    def get_queryset(self, request):
        return self.model.objects.filter(is_province=True)



admin.site.register(ProvinceUser, ProvinceUserAdmin)
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
