# from django.test import TestCase
# from ford3.models.requirements import Requirements
#
#
# class TestRequirements(TestCase):
#     def setUp(self):
#         Requirements.objects.create(
#             id=1,
#             description='Requirement Description',
#             qualification_id=1,
#             assessment=True,
#             interview=True,
#             admission_point_score=24,
#             min_qualification=1234)
#
#     def test_requirement_description(self):
#         newRequirement = Requirements.objects.get(id=1)
#         self.assertEqual(newRequirement.__str__(), 'Requirement Description')
