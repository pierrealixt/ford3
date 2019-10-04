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
        where
            p.id = {provider_id}
            and q.deleted = 'FALSE';
        """.format(provider_id=self.provider.id))

        self.results = [res for res in queryset]

    def get_campus_list(self):
        from ford3.models.campus import Campus
        return set([
            campus.name for campus in Campus.objects.filter(
                provider_id=self.provider.id)
        ])

    def get_subjects_list(self):
        return [
            sub.name for sub in Subject.objects.all()
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
        return ['month', 'year']

    def get_yes_no_list(self):
        return ['Yes', 'No']

    def get_full_part_time_list(self):
        return ['Full time', 'Part time']

    def write_saqa_qualification_name(self, obj, kwargs={}):
        return obj.saqa_qualification.name

    def write_saqa_qualification_saqa_id(self, qualification, kwargs={}):
        return qualification.saqa_qualification.saqa_id

    def write_qualification_name(self, qualification, kwargs={}):
        return qualification.name

    def write_campus_name(self, obj, kwargs={}):
        return obj.campus.name

    def read_campus_name(self, obj, kwargs={}):
        return Campus.objects.get(name=obj)

    def write_occupation_name(self, qualification, kwargs={}):
        try:
            return qualification.occupations.all()[kwargs['index']].name
        except IndexError:
            return None

    def write_qualification_short_description(self, qualification, kwargs={}):
        return qualification.short_description

    def write_qualification_long_description(self, qualification, kwargs={}):
        return qualification.long_description

    def write_interest_name(self, qualification, kwargs={}):
        try:
            return qualification.interests.all()[kwargs['index']].name
        except IndexError:
            return None

    def write_qualification_distance_learning(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.distance_learning,
            self.get_yes_no_list())

    def write_qualification_full_part_time(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.full_time,
            self.get_full_part_time_list())

    def write_qualification_entrance_requirement_subject_subject(self, qualification, kwargs={}):
        return qualification.qualificationentrancerequirementsubject_set.all()[kwargs['index']].subject.name

    def write_qualification_entrance_requirement_subject_minimum_score(self, qualification, kwargs={}):
        return qualification.qualificationentrancerequirementsubject_set.all()[kwargs['index']].minimum_score

    def write_qualification_total_cost(self, qualification, kwargs={}):
        return qualification.total_cost

    def write_qualification_total_cost_comment(self, qualification, kwargs={}):
        return qualification.total_cost_comment

    def write_qualification_critical_skill(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.critical_skill,
            self.get_yes_no_list())

    def write_qualification_green_occupation(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.green_occupation,
            self.get_yes_no_list())


    def write_qualification_high_demand_occupation(self, qualification, kwargs={}):
        return bool_to_string(
            qualification.high_demand_occupation,
            self.get_yes_no_list())

    def write_requirement_min_nqf_level(self, qualification, kwargs={}):
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

    def write_qualification_webpage(self, qualification, kwargs={}):
        return qualification.http_link

    def write_qualification_duration(self, qualification, kwargs={}):
        return qualification.duration

    def write_qualification_time_repr(self, qualification, kwargs={}):
        return qualification.duration_time_repr

    def write_requirement_interview(self, qualification, kwargs={}):
        if qualification.requirement:
            return bool_to_string(
                qualification.requirement.interview,
                self.get_yes_no_list())
        else:
            return ''

    def write_requirement_portfolio(self, qualification, kwargs={}):
        if qualification.requirement:
            return bool_to_string(
                qualification.requirement.portfolio,
                self.get_yes_no_list())
        else:
            return ''

    def write_requirement_assessment(self, qualification, kwargs={}):
        if qualification.requirement:
            return bool_to_string(
                qualification.requirement.assessment,
                self.get_yes_no_list())
        else:
            return ''

    def write_requirement_portfolio_comment(self, qualification, kwargs={}):
        if qualification.requirement:
            return qualification.requirement.portfolio_comment
        else:
            return ''

    def write_requirement_assessment_comment(self, qualification, kwargs={}):
        if qualification.requirement:
            return qualification.requirement.assessment_comment
        else:
            return ''
