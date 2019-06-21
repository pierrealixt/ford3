from django.test import TestCase
from ford3.models.campus import Campus
from ford3.models.qualification import Qualification
from ford3.completion_audit.completion_audit import CompletionAudit # noqa
from ford3.completion_audit.rules import (
    CAMPUS as CAMPUS_COMPLETION_RULES,
    QUALIFICATION as QUALIFICATION_COMPLETION_RULES
)


class TestCampusCompletionAudit(TestCase):
    fixtures = ['groups', 'sa_provinces', 'test_provider_users', 'test_providers', 'test_campus'] # noqa

    def test_complete_campus(self):
        self.campus = Campus.objects.get(pk=1)

        self.audit = CompletionAudit(
            obj=self.campus,
            rules=CAMPUS_COMPLETION_RULES)

        completion_rate = self.audit.run()

        self.assertEqual(completion_rate, 100)

    def test_incomplete_campus(self):
        self.campus = Campus.objects.get(pk=2)

        self.audit = CompletionAudit(
            obj=self.campus,
            rules=CAMPUS_COMPLETION_RULES)

        completion_rate = self.audit.run()

        self.assertEqual(completion_rate, 16)


class TestQualificationCompletionAudit(TestCase):
    fixtures = ['groups', 'sa_provinces', 'test_provider_users',
                'test_providers', 'test_campus', 'test_qualification',
                'test_requirement']

    def test_complete_qualification(self):
        self.qualification = Qualification.objects.get(pk=1)
        self.audit = CompletionAudit(
            obj=self.qualification,
            rules=QUALIFICATION_COMPLETION_RULES)
        completion_rate = self.audit.run()
        self.assertEqual(completion_rate, 100)

    def test_incomplete_qualification(self):
        self.qualification = Qualification.objects.get(pk=2)

        self.audit = CompletionAudit(
            obj=self.qualification,
            rules=QUALIFICATION_COMPLETION_RULES)

        completion_rate = self.audit.run()

        self.assertEqual(completion_rate, 28)
        self.qualification.assessment = True
        self.qualification.save()

        self.audit = CompletionAudit(
            obj=self.qualification,
            rules=QUALIFICATION_COMPLETION_RULES)

        completion_rate = self.audit.run()

        self.assertEqual(completion_rate, 31)
