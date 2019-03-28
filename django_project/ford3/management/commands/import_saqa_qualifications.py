import csv
from django.core.management.base import BaseCommand
from ford3.models import SubFieldOfStudy, SAQAQualification


class Command(BaseCommand):
    """
    Import SAQA Qualifications from scraped CSV
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            dest='force',
            help='Force execute without asking for input from the user')

    def handle(self, *args, **options):
        force = options.get('force')
        if force:
            yes_to_continue = 'yes'
        else:
            yes_to_continue = input(
                'This will delete all data in the saqa_qualification table '
                'and then attempt a fresh import. Type "yes" to continue.  ')
        if yes_to_continue != 'yes':
            print('Import canceled - User response: ' + yes_to_continue)
            return
        self.delete_everything()
        print('Old data cleared from the saqa_qualification table')
        with open('SAQAData.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    # Create a qualification object for the row
                    saqa_id = row[0]
                    name = row[1]
                    new_saqa_qualification = SAQAQualification()
                    new_saqa_qualification.name = name
                    new_saqa_qualification.saqa_id = saqa_id
                    # Compile subfield of study
                    this_subfield_of_study = ''
                    for x in range(4, 8):
                        if len(row[x]) > 0:
                            this_subfield_of_study += ',' + row[x]

                    # For each subfield of study, get the subfield of study
                    # from the list of subfields of study in the database
                    subfield_of_study_object = SubFieldOfStudy.objects.filter(
                        name = this_subfield_of_study
                    )

                    new_saqa_qualification.sub_field_of_study = (
                        subfield_of_study_object.first())
                    new_saqa_qualification.save()
                    line_count += 1
        print(f'Processed {line_count} lines.')

    def delete_everything(self):
        SAQAQualification.objects.all().delete()
