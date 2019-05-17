from django.test import TestCase
from ford3.management.commands.import_saqa_qualifications import parse_line
from ford3.models.saqa_qualification import SAQAQualification
from ford3.models.field_of_study import FieldOfStudy


class TestImportSaqaQualifications(TestCase):
    def setUp(self):
        self.csv_line = '59731;Further Education and Training Certificate: Mechanical Handling (Rigging);Further Ed and Training Cert;Manufacturing, Engineering and Technology;Engineering and Related Design;;' # noqa
        self.csv_line = self.csv_line.split(';')
        self.line = parse_line(self.csv_line)

    def test_parse_line(self):
        self.assertEqual(self.line.saqa_id, '59731')
        self.assertEqual(self.line.field_of_study, 'Manufacturing, Engineering and Technology') # noqa
        self.assertEqual(self.line.subfield_of_study, 'Engineering and Related Design') # noqa

    def test_create_saqa_qualif(self):
        self.assertEqual(len(SAQAQualification.objects.all()), 0)

        SAQAQualification.get_or_create_accredited(self.line._asdict())

        self.assertEqual(len(SAQAQualification.objects.all()), 1)

    def test_get_saqa_qualif(self):
        self.assertEqual(len(SAQAQualification.objects.all()), 0)

        SAQAQualification.get_or_create_accredited(self.line._asdict())

        SAQAQualification.get_or_create_accredited(self.line._asdict())
        self.assertEqual(len(SAQAQualification.objects.all()), 1)

    def test_create_and_attach_field_of_study(self):
        saqa_qualif = SAQAQualification.get_or_create_accredited(
            self.line._asdict())

        fos, created = FieldOfStudy.objects.get_or_create(
            name=self.line.field_of_study)
        self.assertTrue(created)
        saqa_qualif.field_of_study = fos

        saqa_qualif.save()

        self.assertEqual(
            saqa_qualif.field_of_study.name,
            self.line.field_of_study)

    def test_get_and_attach_field_of_study(self):
        saqa_qualif = SAQAQualification.get_or_create_accredited(
            self.line._asdict())

        fos, created = FieldOfStudy.objects.get_or_create(
            name=self.line.field_of_study)
        self.assertTrue(created)

        fos, created = FieldOfStudy.objects.get_or_create(
            name=self.line.field_of_study)
        self.assertFalse(created)

        saqa_qualif.field_of_study = fos

        saqa_qualif.save()

        self.assertEqual(
            saqa_qualif.field_of_study.name,
            self.line.field_of_study)
