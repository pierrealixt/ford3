from django.apps import apps
from decimal import Decimal


def update_qualification(row):
    qualification_model = apps.get_model('ford3', 'Qualification')
    qualification_id = row['qualification__id']
    qualif = qualification_model.objects.get(
        id=qualification_id)
    models = get_models(qualif)

    true = 'Yes'
    full_time = 'Full time'

    diffs = {}
    try:
        diffs = {
            'campus__id': {
                'old': qualif.campus.id,
                'new': qualif.campus.id
            },
            'campus__name': {
                'old': row['campus__name'],
                'new': row['campus__name']
            },
            'qualification__id': {
                'old': row['qualification__id'],
                'new': row['qualification__id']
            },
            'saqa_qualification__name': {
                'old': row['saqa_qualification__name'],
                'new': row['saqa_qualification__name']
            },
            'saqa_qualification__saqa_id': {
                'old': row['saqa_qualification__saqa_id'],
                'new': row['saqa_qualification__saqa_id']
            },
            'qualification__deleted': {
                'name': 'deleted',
                'old': qualif.deleted,
                'new': true != row['qualification__deleted']
            },
            'qualification__short_description': {
                'name': 'short_description',
                'old': qualif.short_description,
                'new': row['qualification__short_description']
            },
            'qualification__long_description': {
                'name': 'long_description',
                'old': qualif.long_description,
                'new': row['qualification__long_description']
            },
            'qualification__distance_learning': {
                'name': 'distance_learning',
                'old': qualif.distance_learning,
                'new': true == row['qualification__distance_learning']
            },
            'qualification__full_part_time': {
                'name': 'full_time',
                'old': qualif.full_time,
                'new': full_time == row['qualification__full_part_time']
            },
            'qualification__webpage': {
                'name': 'http_link',
                'old': qualif.http_link,
                'new': row['qualification__webpage']
            },
            'qualification__duration': {
                'name': 'duration',
                'old': qualif.duration,
                'new': row['qualification__duration']
            },
            'qualification__time_repr': {
                'name': 'duration_time_repr',
                'old': qualif.duration_time_repr,
                'new': row['qualification__time_repr']
            },
            'qualification__total_cost': {
                'name': 'total_cost',
                'old': float(qualif.total_cost) if isinstance(qualif.total_cost, Decimal) else None,  # noqa
                'new': float(row['qualification__total_cost']) if row['qualification__total_cost'] is not None else None  # noqa
            },
            'qualification__total_cost_comment': {
                'name': 'total_cost_comment',
                'old': qualif.total_cost_comment,
                'new': row['qualification__total_cost_comment']
            },
            'qualification__critical_skill': {
                'name': 'critical_skill',
                'old': qualif.critical_skill,
                'new': true == row['qualification__critical_skill']
            },
            'qualification__green_occupation': {
                'name': 'green_occupation',
                'old': qualif.green_occupation,
                'new': true == row['qualification__green_occupation']
            },
            'qualification__high_demand_occupation': {
                'name': 'high_demand_occupation',
                'old': qualif.high_demand_occupation,
                'new': true == row['qualification__high_demand_occupation']
            },
            'requirement__min_nqf_level': {
                'name': 'min_nqf_level',
                'old': qualif.requirement.min_nqf_level,
                'new': row['requirement__min_nqf_level']
            },
            'requirement__interview': {
                'name': 'interview',
                'old': qualif.requirement.interview,
                'new': true == row['requirement__interview']
            },
            'requirement__portfolio': {
                'name': 'portfolio',
                'old': qualif.requirement.portfolio,
                'new': true == row['requirement__portfolio']
            },
            'requirement__portfolio_comment': {
                'name': 'portfolio_comment',
                'old': qualif.requirement.portfolio_comment,
                'new': row['requirement__portfolio_comment']
            },
            'requirement__assessment': {
                'name': 'assessment',
                'old': qualif.requirement.assessment,
                'new': true == row['requirement__assessment']
            },
            'requirement__assessment_comment': {
                'name': 'assessment_comment',
                'old': qualif.requirement.assessment_comment,
                'new': row['requirement__assessment_comment']
            },
            'requirement__require_aps_score': {
                'name': 'require_aps_score',
                'old': qualif.requirement.require_aps_score,
                'new': true == row['requirement__require_aps_score']
            },
            'requirement__require_certain_subjects': {
                'name': 'require_certain_subjects',
                'old': qualif.requirement.require_certain_subjects,
                'new': true == row['requirement__require_certain_subjects']
            }
        }
    except KeyError:
        pass

    for key, values in diffs.items():
        if values['old'] != values['new']:
            if 'qualification' in key:
                model = models['qualification']
            elif 'requirement' in key:
                model = models['requirement']

            setattr(model, values['name'], values['new'])
            model.save()

    # hack qualification__deleted
    # if True, it is deleted.
    # in UI: Is it still active? Yes means it is not deleted (False)...
    try:
        diffs['qualification__deleted']['old'] = not diffs['qualification__deleted']['old']  # noqa
        diffs['qualification__deleted']['new'] = not diffs['qualification__deleted']['new']  # noqa
    except KeyError:
        pass

    try:
        if diffs['qualification__full_part_time']['old']:
            diffs['qualification__full_part_time']['old'] = 'Full time'
        else:
            diffs['qualification__full_part_time']['old'] = 'Part time'

        if diffs['qualification__full_part_time']['new']:
            diffs['qualification__full_part_time']['new'] = 'Full time'
        else:
            diffs['qualification__full_part_time']['new'] = 'Part time'
    except KeyError:
        pass

    try:
        if diffs['qualification__total_cost']['old']:
            diffs['qualification__total_cost']['old'] = f"R {int(diffs['qualification__total_cost']['old'])}"  # noqa

        if diffs['qualification__total_cost']['new']:
            diffs['qualification__total_cost']['new'] = f"R {int(diffs['qualification__total_cost']['new'])}"  # noqa
    except KeyError:
        pass
    # admission point score
    try:
        people_group_model = apps.get_model('ford3', 'PeopleGroup')
        people_groups = people_group_model.objects.all().order_by('id')
        base_key = 'admission_point_score'
        aps_diffs = {}
        qualif_aps = qualif.requirement.admissionpointscore_set\
            .all().order_by('id')

        aps_rows = [field for field in row if base_key in field]
        for index, row_key in enumerate(aps_rows):
            try:
                aps = qualif_aps[index]
                old_value = aps.value
                aps.value = row[row_key]
                aps.save()
            except IndexError:
                old_value = None
                qualif.requirement.admissionpointscore_set.create(
                    people_group=people_groups[index],
                    value=row[row_key]
                )

            aps_diffs[row_key] = {
                'old': old_value,
                'new': row[row_key]
            }

        diffs.update(aps_diffs)
    except KeyError:
        pass
    except Exception as e:
        raise e

    # subjects
    try:
        subjects_with_score = [
            {
                'name': row[f'qualification_entrance_requirement_subject__subject--{index}'],  # noqa
                'score': row[f'qualification_entrance_requirement_subject__minimum_score--{index}']  # noqa
            }
            for index in range(1, 5)
        ]
        subjects_with_score.insert(0,
            {
                'name': row['qualification_entrance_requirement_subject__subject'],  # noqa
                'score': row['qualification_entrance_requirement_subject__minimum_score']  # noqa
            }
        )

        subject_model = apps.get_model('ford3', 'Subject')

        qualif_subjects = qualif.qualificationentrancerequirementsubject_set\
            .all().order_by('id')

        subjects_with_score_diffs = {}
        for index, subject in enumerate(subjects_with_score):
            if index == 0:
                keys = {
                    'subject': 'qualification_entrance_requirement_subject__subject',  # noqa
                    'score': 'qualification_entrance_requirement_subject__minimum_score'  # noqa
                }
            else:
                keys = {
                    'subject': f'qualification_entrance_requirement_subject__subject--{index}',  # noqa
                    'score': f'qualification_entrance_requirement_subject__minimum_score--{index}'  # noqa
                }

            if subject['name'] is None:
                subjects_with_score_diffs[keys['subject']] = {
                    'old': None,
                    'new': None
                }
                subjects_with_score_diffs[keys['score']] = {
                    'old': None,
                    'new': None
                }

                continue

            import re
            subject_id = re.findall("[\\W]([\\d]+)", subject['name'])[0]

            subject_ins = subject_model.objects.get(id=subject_id)

            try:
                qualif_subject = qualif_subjects[index]

                old_subject_name = f'{qualif_subject.subject.name} ({qualif_subject.subject.id})'  # noqa
                old_subject_score = qualif_subject.minimum_score

                qualif_subject.subject = subject_ins
                qualif_subject.minimum_score = subject['score']
                qualif_subject.save()
            except IndexError:
                old_subject_name = None
                old_subject_score = None

                qualif.qualificationentrancerequirementsubject_set.create(
                    subject=subject_ins,
                    minimum_score=subject['score']
                )

            subjects_with_score_diffs[keys['subject']] = {
                'old': old_subject_name,
                'new': f'{subject_ins.name} ({subject_ins.id})'
                # subject['name']
            }
            subjects_with_score_diffs[keys['score']] = {
                'old': old_subject_score,
                'new': subject['score']
            }

        diffs.update(subjects_with_score_diffs)
    except KeyError:
        pass

    try:
        # occupations
        qualif_occupations = qualif.occupations.all().order_by('id')

        base_key = 'occupation__name'

        occupation_model = apps.get_model('ford3', 'Occupation')
        occupation_diffs = {}
        occupation_ids = []
        for index in range(0, 5):
            if index == 0:
                key = base_key
            else:
                key = f'{base_key}--{index}'

            try:
                old_value = qualif_occupations[index].name
            except IndexError:
                old_value = None

            new_value = row[key]

            try:
                occ = occupation_model.objects.get(name=new_value)
                occupation_ids.append(occ.id)
            except occupation_model.DoesNotExist:
                new_value = None

            occupation_diffs[key] = {
                'old': old_value,
                'new': new_value
            }

        if len(occupation_ids) > 0:
            qualif.toggle_occupations(' '.join([
                str(occ_id) for occ_id in list(occupation_ids)
            ]))

        diffs.update(occupation_diffs)
    except KeyError:
        pass

    try:
        # interests
        interest_model = apps.get_model('ford3', 'Interest')
        base_key = 'interest__name'
        interest_diffs = {}
        qualif_interests = qualif.interests.all().order_by('id')

        for index in range(0, 3):
            if index == 0:
                key = base_key
            else:
                key = f'{base_key}--{index}'

            try:
                old_value = qualif_interests[index].name
            except IndexError:
                old_value = None

            new_value = row[key]

            try:
                interest = interest_model.objects.get(name=new_value)
                qualif.interests.add(interest)
            except interest_model.DoesNotExist:
                new_value = None

            interest_diffs[key] = {
                'old': old_value,
                'new': new_value
            }

        diffs.update(interest_diffs)
    except:
        pass

    from django.shortcuts import reverse

    completion = {
        'published': qualif.published,
        'ready_to_publish': qualif.ready_to_publish,
        'completion_rate': qualif.completion_rate,
        'link': reverse('publish-qualification', kwargs={
            'provider_id': qualif.campus.provider.id,
            'campus_id': qualif.campus.id,
            'qualification_id': qualif.id
        })
    }
    return True, diffs, completion


def get_models(current_qualification):
    models = {}
    models['campus'] = current_qualification.campus
    models['saqa_qualification'] = current_qualification.saqa_qualification
    models['qualification'] = current_qualification
    models['requirement'] = current_qualification.requirement

    if not models['requirement']:
        requirement = (apps.get_model('ford3', 'Requirement'))()
        requirement.qualification_id = current_qualification.id
        requirement.save()
        models['requirement'] = requirement

    return models
