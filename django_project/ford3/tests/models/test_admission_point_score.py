from django.test import TestCase
from ford3.models.requirement import Requirement
from ford3.models.people_group import PeopleGroup
from ford3.models.admission_point_score import AdmissionPointScore


class TestAdmissionPointScore(TestCase):

    fixtures = [
        'sa_provinces', 'groups',
        'test_provider_users',
        'test_providers', 'test_campus',
        'test_qualification', 'test_requirement', 'people_groups']

    def setUp(self):
        self.requirement = Requirement.objects.get(pk=1)

    def test_no_admission_point_scores(self):
        without_id = [
            {
                'id': aps['id'],
                'value': aps['value'],
                'group': {
                    'name': aps['group']['name']
                }
            }
            for aps in self.requirement.admission_point_scores
        ]
        self.assertEqual(without_id, [
            {'id': 0, 'value': 0, 'group':
                {'name': 'Previously disadvantaged'}},
            {'id': 0, 'value': 0, 'group':
                {'name': 'No disadvantaged'}},
            {'id': 0, 'value': 0, 'group':
                {'name': 'International students'}}
        ])

    def test_only_one_admission_point_score(self):
        inter_students = PeopleGroup.objects.get(
            group='International students')

        aps = AdmissionPointScore()
        aps.people_group = inter_students
        aps.requirement = self.requirement
        aps.value = 42
        aps.save()

        without_id = [
            {
                'id': aps['id'],
                'value': aps['value'],
                'group': {
                    'name': aps['group']['name']
                }
            }
            for aps in self.requirement.admission_point_scores
        ]

        self.assertEqual(without_id, [
            {'id': 0, 'value': 0, 'group':
                {'name': 'Previously disadvantaged'}},
            {'id': 0, 'value': 0, 'group':
                {'name': 'No disadvantaged'}},
            {'id': aps.id, 'value': aps.value, 'group':
                {'name': 'International students'}}
        ])

    def test_add_people_group(self):
        self.assertEqual(len(self.requirement.admission_point_scores), 3)

        french_group = PeopleGroup()
        french_group.group = 'French students'
        french_group.save()

        self.assertEqual(len(self.requirement.admission_point_scores), 4)
