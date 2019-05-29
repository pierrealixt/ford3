from django.test import TestCase
from ford3.models.user import User



class TestUser(TestCase):
    def test_edu_group(self):
        user = User(
            email='email',
            is_province=True
        )

        self.assertEqual(user.edu_group.name.lower(), 'province')
        self.assertEqual(user.edu_group.value, 1)

        user = User(
            email='email',
            is_provider=True
        )
        self.assertEqual(user.edu_group.name.lower(), 'provider')
        self.assertEqual(user.edu_group.value, 2)

        user = User(
            email='email',
            is_campus=True
        )
        self.assertEqual(user.edu_group.name.lower(), 'campus')
        self.assertEqual(user.edu_group.value, 3)


