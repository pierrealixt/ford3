import csv
from collections import namedtuple
from django.core.management.base import BaseCommand
from ford3.models import (
    SAQAQualification,
    FieldOfStudy,
    SubFieldOfStudy
)


def parse_line(csv_line):
    Line = namedtuple('Line', [
        'saqa_id',
        'name',
        'type',
        'field_of_study',
        'subfield_of_study'])
    return Line(*csv_line[0:5])


class Command(BaseCommand):
    """
    Import SAQA Qualifications from scraped CSV
    """
    def handle(self, *args, **options):
        with open('SAQAData.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    line = parse_line(row)

                    saqa_qualif = SAQAQualification.get_or_create_accredited(
                        line._asdict())

                    fos, created = FieldOfStudy.objects.get_or_create(
                        name=line.field_of_study)

                    sfos, created = SubFieldOfStudy.objects.get_or_create(
                        name=line.subfield_of_study,
                        field_of_study=fos)

                    saqa_qualif.field_of_study = fos
                    saqa_qualif.sub_field_of_study = sfos

                    saqa_qualif.save()

                    line_count += 1
        print(f'Processed {line_count} lines.')
