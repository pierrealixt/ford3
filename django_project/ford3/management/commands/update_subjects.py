import itertools
from django.core.management.base import BaseCommand
from django.db.models.deletion import ProtectedError
from ford3.models.subject import Subject
from ford3.models.qualification_entrance_requirement_subject import QualificationEntranceRequirementSubject # noqa


class Command(BaseCommand):
    def handle(self, *args, **options):
        # add languages
        for lng in ['English', 'Afrikaans', 'IsiNdebele', 'IsiXhosa', 'IsiZulu', 'Sepedi', 'Sesotho', 'Setswana', 'Xitstonga', 'Tshivenda', 'SeSwati']:
            if not Subject.objects.filter(name=lng).exists():
                print(f'Creating {lng}')
                s = Subject()
                s.name = lng
                s.is_language = True
                s.save()

        # remove "Home language" and "First additional language"
        for lng in ['Home language', 'First additional language']:
            try:
                subject = Subject.objects.get(name=lng)
                subject.delete()
                print(f'{lng} deleted')
            except Subject.DoesNotExist:
                print(f'{lng} does not exist')
                pass
            except ProtectedError:
                QualificationEntranceRequirementSubject.objects.filter(
                    subject=subject).delete()
                subject.delete()
                print(f'{lng} deleted with dependencies')

        # add "Any other subject" three times
        subject_name = "Any other subject"
        if Subject.objects.filter(name=subject_name).count() == 0:
            for _ in itertools.repeat(None, 3):
                s = Subject(
                    name=subject_name,
                    is_other=True)
                s.save()
            assert Subject.objects.filter(name=subject_name).count(), 3
            print('Added "Any other subject" 3 times')
