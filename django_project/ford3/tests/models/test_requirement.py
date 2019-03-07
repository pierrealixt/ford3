from django.test import TestCase
from ford3.tests.models.model_factories import ModelFactories


class TestRequirement(TestCase):

    def test_requirement_description(self):
        new_requirement = ModelFactories.get_requirement_test_object()
        self.assertEqual(new_requirement.__str__(),
            """Some long description that goes on..."""
        )
