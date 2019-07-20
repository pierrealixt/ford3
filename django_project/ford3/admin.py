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
    Province,
    PeopleGroup
)


# bypass provider form validation in the Django Administration
class ProviderAdminForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'province']


class ProviderAdmin(admin.ModelAdmin):
    form = ProviderAdminForm


admin.site.register(Provider, ProviderAdmin)


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'is_staff',
            'is_superuser',
            'is_province',
            'is_provider',
            'is_campus']


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = (
        'email', 'edu_group_name',
        'is_active', 'first_name', 'last_name',
        'get_groups'
    )

    def edu_group_name(self, instance):
        if type(instance.edu_group) == bool:
            return 'Admin'
        return instance.edu_group.name

    def get_groups(self, obj):
        return "\n".join([p.name for p in obj.groups.all()])


admin.site.register(User, UserAdmin)


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
        return "\n".join([p.name for p in obj.provinces.all()])

    def get_queryset(self, request):
        return self.model.objects.filter(is_province=True)


admin.site.register(ProvinceUser, ProvinceUserAdmin)
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
admin.site.register(PeopleGroup)
