# coding=utf-8
"""Factory for building model instances for testing."""

from ford3.models.campus import Campus
from ford3.models.field_of_study import FieldOfStudy
from ford3.models.module import Module
from ford3.models.occupation import Occupation
from ford3.models.provider import Provider
from ford3.models.qualification import Qualification
from ford3.models.requirement import Requirement
from ford3.models.secondary_institution_type import SecondaryInstitutionType
from ford3.models.sub_field_of_study import SubFieldOfStudy
from ford3.models.subject import Subject


class ModelFactories:
    @staticmethod
    def get_qualification_test_object(new_id=1):
        qualification_test_object_instance = Qualification.objects.create(
            id=new_id,
            qualification_id=1,
            saqa_id=4,
            name='Object Test Name',
            short_description='Some short description',
            long_description='Some very long description that just goes on...',
            nqf_level=6,
            duration_in_months=12,
            full_time=True,
            part_time=False,
            credits_after_completion=200,
            distance_learning=False,
            estimated_annual_fee=100000,
            occupation_id=ModelFactories.get_occupation_test_object(),
            campus_id=ModelFactories.get_campus_test_object(),
            sub_field_of_study_id=(
                ModelFactories.get_sub_field_of_study_test_object()))
        qualification_test_object_instance.modules.add(
            ModelFactories.get_module_test_object(1))

        return qualification_test_object_instance

    @staticmethod
    def get_requirement_test_object(new_id=1):
        requirement_test_object_instance = Requirement.objects.create(
            id=new_id,
            description='Some long description that goes on...',
            qualification_id=ModelFactories.get_qualification_test_object(),
            assessment=True,
            interview=True,
            admission_point_score=24,
            min_qualification=1234)

        return requirement_test_object_instance

    @staticmethod
    def get_secondary_institution_type_test_object(new_id=1):
        secondary_institution_type_test_object_instance = \
            SecondaryInstitutionType.objects.create(
                id=new_id,
                name='Object Test Name'
            )
        return secondary_institution_type_test_object_instance

    @staticmethod
    def get_campus_test_object(new_id=1):
        campus_test_object_instance = Campus.objects.create(
            id=new_id,
            provider_id=ModelFactories.get_provider_test_object(),
            name='Object Test Name',
        )

        return campus_test_object_instance

    @staticmethod
    def get_module_test_object(new_id=1):
        module_test_object_instance = Module.objects.create(
            id=new_id,
            name='Object Test Name',
            description='Some long description that goes on...'
        )

        return module_test_object_instance

    @staticmethod
    def get_field_of_study_test_object(new_id=1):
        field_of_study_test_object_instance = FieldOfStudy.objects.create(
            id=new_id,
            name='Object Test Name'
        )

        return field_of_study_test_object_instance

    @staticmethod
    def get_occupation_test_object(new_id=1):
        occupation_test_object_instance = Occupation.objects.create(
            id=new_id,
            name='Object Test Name',
            description='Some long description that goes on...'
        )

        return occupation_test_object_instance

    @staticmethod
    def get_provider_test_object(new_id=1):
        provider_test_object_instance = Provider.objects.create(
            id=new_id,
            name='Object Test Name',
            website='www.mytest.com',
            logo_url='http://sometestplaceholder/logo.png',
            email='Test@test.com',
            admissions_contact_no='0137527576',
            postal_address='1200'
        )

        return provider_test_object_instance

    @staticmethod
    def get_sub_field_of_study_test_object(new_id=1):
        sub_field_of_study_test_object_instance = (
            SubFieldOfStudy.objects.create(
                id=new_id,
                name='Object Test Name',
                field_of_study_id=(
                    ModelFactories.get_field_of_study_test_object(1)),
            ))

        return sub_field_of_study_test_object_instance

    @staticmethod
    def get_subject_test_object(new_id=1):
        subject_field_of_study_test_object = Subject.objects.create(
            id=new_id,
            name='Object Test Name',
            description='Some long description that goes on'
        )

        return subject_field_of_study_test_object
