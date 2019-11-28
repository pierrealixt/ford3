from ford3.models.interest import Interest
from ford3.models.subject import Subject
from ford3.models.occupation import Occupation
from ford3.models.campus import Campus
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel


def bool_to_string(boolean, choices):
    if boolean:
        return choices[0]
    else:
        return choices[1]


class OpenEduSmartExcelData():
    def __init__(self, provider_id):
        from ford3.models.provider import Provider

        from ford3.models.qualification import Qualification

        self.provider = Provider.objects.get(pk=provider_id)

        queryset = Qualification.objects.raw("""
        select q.*
            from ford3_qualification q
            INNER JOIN  ford3_campus c on c.id = q.campus_id
            INNER JOIN ford3_provider p on p.id = c.provider_id
            INNER JOIN ford3_saqaqualification sq on sq.id = q.saqa_qualification_id
        where
            p.id = {provider_id}
            and
                NOT c.deleted
        order by
            q.deleted, sq.saqa_id DESC;
        """.format(provider_id=self.provider.id))  # noqa
        self.results = [res for res in queryset]

    def get_campus_list(self):
        from ford3.models.campus import Campus
        return set([
            campus.name for campus in Campus.objects.filter(
                provider_id=self.provider.id)
        ])

    def get_subjects_list(self):
        return [
            f'{sub.name} ({sub.id})' for sub in Subject.objects.all()
        ]

    def get_occupations_list(self):
        return [
            occ.name for occ in Occupation.objects.all()
        ]

    def get_interests_list(self):
        return [
            interest.name for interest in Interest.objects.all()
        ]

    def get_qualification_time_repr_list(self):
        return ['Month(s)', 'Year(s)']

    @classmethod
    def get_yes_no_list(self):
        return ['Yes', 'No']

    @classmethod
    def get_full_part_time_list(self):
        return ['Full time', 'Part time']

    def write_qualification__deleted(self, obj, kwargs={}):
        return bool_to_string(
            not obj.deleted,
            self.get_yes_no_list())

    def write_saqa_qualification__name(self, obj, kwargs={}):
        return obj.saqa_qualification.name

    def write_saqa_qualification__saqa_id(self, qualification, kwargs={}):
        return qualification.saqa_qualification.saqa_id

    def write_qualification__id(self, qualification, kwargs={}):
        if qualification.id:
            return qualification.id
        else:
            return ''

    def write_qualification__name(self, qualification, kwargs={}):
        return qualification.name

    def write_campus__name(self, obj, kwargs={}):
        return obj.campus.name

    def read_campus__name(self, obj, kwargs={}):
        return Campus.objects.get(name=obj)

    def write_occupation__name(self, qualification, kwargs={}):
        try:
            return qualification.occupations\
                .all()\
                .order_by('id')[kwargs['index']].name
        except IndexError:
            return None

    def write_qualification__short_description(self, qualification, kwargs={}):
        return qualification.short_description

    def write_qualification__long_description(self, qualification, kwargs={}):
        return qualification.long_description

    def write_interest__name(self, qualification, kwargs={}):
        try:
            return qualification.interests\
                .all()\
                .order_by('id')[kwargs['index']].name
        except IndexError:
            return None

    def write_qualification__distance_learning(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.distance_learning,
            self.get_yes_no_list())

    def write_qualification__full_part_time(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.full_time,
            self.get_full_part_time_list())

    def write_qualification_entrance_requirement_subject__subject(
        self, qualification, kwargs={}):

        subject = qualification.qualificationentrancerequirementsubject_set\
            .all().order_by('id')[kwargs['index']].subject
        return f'{subject.name} ({subject.id})'

    def write_qualification_entrance_requirement_subject__minimum_score(
        self, qualification, kwargs={}):

        return qualification.qualificationentrancerequirementsubject_set\
            .all().order_by('id')[kwargs['index']].minimum_score

    def write_qualification__total_cost(self, qualification, kwargs={}):
        return qualification.total_cost

    def write_qualification__total_cost_comment(
        self, qualification, kwargs={}):
        return qualification.total_cost_comment

    def write_qualification__critical_skill(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.critical_skill,
            self.get_yes_no_list())

    def write_qualification__green_occupation(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.green_occupation,
            self.get_yes_no_list())


    def write_qualification__high_demand_occupation(
        self, qualification, kwargs={}):

        return bool_to_string(
            qualification.high_demand_occupation,
            self.get_yes_no_list())

    def write_requirement__min_nqf_level(self, qualification, kwargs={}):
        try:
            if qualification.requirement:
                level = qualification.requirement.min_nqf_level.split('.')[1]
                return SaqaQualificationLevel[level].value
            else:
                return ''
        except Exception:
            return ''

    def get_required_entrance_qualification_list(self):
        return [
            level.value for level in SaqaQualificationLevel
        ]

    def write_qualification__webpage(self, qualification, kwargs={}):
        return qualification.http_link

    def write_qualification__duration(self, qualification, kwargs={}):
        return qualification.duration

    def write_qualification__time_repr(self, qualification, kwargs={}):
        return qualification.duration_time_repr

    def write_requirement__interview(self, qualification, kwargs={}):
        if qualification.requirement:
            return bool_to_string(
                qualification.requirement.interview,
                self.get_yes_no_list())
        else:
            return ''

    def write_requirement__portfolio(self, qualification, kwargs={}):
        if qualification.requirement:
            return bool_to_string(
                qualification.requirement.portfolio,
                self.get_yes_no_list())
        else:
            return ''

    def write_requirement__assessment(self, qualification, kwargs={}):
        if qualification.requirement:
            return bool_to_string(
                qualification.requirement.assessment,
                self.get_yes_no_list())
        else:
            return ''

    def write_requirement__portfolio_comment(self, qualification, kwargs={}):
        if qualification.requirement:
            return qualification.requirement.portfolio_comment
        else:
            return ''

    def write_requirement__assessment_comment(self, qualification, kwargs={}):
        if qualification.requirement:
            return qualification.requirement.assessment_comment
        else:
            return ''

    def write_requirement__require_aps_score(self, qualification, kwargs={}):
        if qualification.requirement:
            return bool_to_string(
                qualification.requirement.require_aps_score,
                self.get_yes_no_list())
        else:
            return ''

    def write_get_number_of_people_groups(self):
        from ford3.models.people_group import PeopleGroup
        return PeopleGroup.objects.count()

    def write_get_name_of_people_group(self, qualification, kwargs={}):
        from ford3.models.people_group import PeopleGroup
        return PeopleGroup.objects.all().order_by('id')[kwargs['index']].group

    def write_admission_point_score__value(self, qualification, kwargs={}):
        if qualification.requirement:
            return qualification\
                .requirement.admission_point_scores[kwargs['index']]['value']
        else:
            return ''

    def write_requirement__require_certain_subjects(
        self, qualification, kwargs={}):

        if qualification.requirement:
            return bool_to_string(
                qualification.requirement.require_certain_subjects,
                self.get_yes_no_list())
        else:
            return ''
