from django.test import TestCase
from ford3.models_logic.qualification_audit import QualificationAudit
from ford3.tests.models.model_factories import ModelFactories
from ford3.models.qualification import Qualification


class TestQualificationAudit(TestCase):

    def setUp(self):
        self.qualification = ModelFactories.get_qualification_test_object()
        self.empty_qualification = Qualification()
        self.requirement = ModelFactories.get_requirement_test_object()
        self.requirement.qualification = self.qualification
        self.requirement.save()
        self.qa = QualificationAudit(self.qualification)
        self.empty_qa = QualificationAudit(self.empty_qualification)

    def test_audit_short_description(self):
        self.assertFalse(self.empty_qa.audit_short_description())
        self.assertTrue(self.qa.audit_short_description())
        self.qualification.short_description = ""
        self.qualification.save()
        self.assertFalse(self.qa.audit_short_description())

    def test_evaluate_audit_empty(self):
        self.assertFalse(self.empty_qa.evaluate_audit())

    def test_audit_full_time_part_time(self):
        self.assertFalse(self.empty_qa.audit_full_time())
        self.assertTrue(self.qa.audit_full_time())

    def test_audit_min_nqf_level(self):
        self.assertFalse(self.empty_qa.audit_min_nqf_level())
        self.requirement.min_nqf_level = 1
        self.requirement.save()
        self.assertTrue(self.qa.audit_min_nqf_level())

    def test_audit_required_subjects(self):
        self.assertFalse(self.qa.audit_required_subjects())
        self.requirement.require_certain_subjects = True
        self.requirement.save()
        self.subject1 = (
            ModelFactories.get_qualification_entrance_requirement_to())
        self.subject1.qualification = self.qualification
        self.subject1.save()
        self.assertTrue(self.qa.audit_required_subjects())

    def test_audit_occupations(self):
        self.assertFalse(self.empty_qa.audit_occupations())
        self.assertTrue(self.qa.audit_occupations())

    def test_save_qualification_runs_audit(self):
        self.assertFalse(self.qualification.ready_to_publish)
        self.requirement.require_certain_subjects = True
        self.requirement.save()
        self.subject1 = (
            ModelFactories.get_qualification_entrance_requirement_to())
        self.subject1.qualification = self.qualification
        self.subject1.save()
        self.qualification.short_description = "Something"
        self.qualification.save()
        self.assertTrue(self.qualification.ready_to_publish)
