# coding=utf-8
"""Factory for building model instances for testing."""
import datetime
from ford3.models.campus import Campus
from ford3.models.field_of_study import FieldOfStudy
from ford3.models.occupation import Occupation
from ford3.models.provider import Provider
from ford3.models.qualification import Qualification
from ford3.models.requirement import Requirement
from ford3.models.secondary_institution_type import SecondaryInstitutionType
from ford3.models.sub_field_of_study import SubFieldOfStudy
from ford3.models.subject import Subject
from ford3.models.campus_event import CampusEvent
from ford3.models.qualification_event import  QualificationEvent
from ford3.models.interest import Interest


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
            total_cost=100000,
            occupation_id=ModelFactories.get_occupation_test_object(),
            campus_id=ModelFactories.get_campus_test_object(),
            sub_field_of_study_id=(
                ModelFactories.get_sub_field_of_study_test_object()),
            completion_rate=72,
            total_cost_comment='Way too much',
            critical_skill=False,
            green_occupation=True,
            high_demand_occupation=False,
            )

        
        qualification_test_object_instance.interests.add(
            ModelFactories.get_interest_test_object());
        print(qualification_test_object_instance.interests)
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
            min_qualification=1234,
            portfolio=False,
            portfolio_comment='Optional if available',
            aps_calculator_link='http://apscalculator.nr')

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
            photo_url= 'Is this going to be base64 encoded?',
            telephone='+27137441422',
            email='test@campus.com',
            max_students_per_year='42',
            physical_address='24 Test Street, Extension Test, TestVille',
            postal_address='Email us rather')

        return campus_test_object_instance

    @staticmethod
    def get_campus_event_test_object(new_id=1):
        campus_event_test_object_instance = CampusEvent.objects.create(
            id=new_id,
            campus_id=ModelFactories.get_campus_test_object(),
            name='Campus Event Test Name',
            date_start=datetime.date(2019, 3, 6),
            date_end=datetime.date(2019, 8, 9),
            http_link='http://www.google.com')

        return campus_event_test_object_instance

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
            postal_address='1200',
            physical_address='Some long physical address',
            telephone='27821233322',
            provider_type='Technicon',
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

    @staticmethod
    def get_qualification_event_test_object(new_id=1):
        qualification_event_test_object = QualificationEvent.objects.create(
            id=new_id,
            qualification_id=ModelFactories.get_qualification_test_object(),
            name='Qualification Event Test Name',
            date_start=datetime.date(2019, 3, 6),
            date_end=datetime.date(2019, 8, 9),
            http_link='http://www.google.com')

        return qualification_event_test_object

    @staticmethod
    def get_interest_test_object(new_id=1):
        interest_test_object = Interest.objects.create(
            id=new_id,
            name='Interest name'
        )
