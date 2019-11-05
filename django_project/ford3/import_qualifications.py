from django.apps import apps

MODEL_DELIMITER = '__'
ITERATION_DELIMITER = '--'


def import_excel_data(row):
    errors = {}
    diffs = {}
    qualification_model = apps.get_model('ford3', 'Qualification')

    qualification_id = row['qualification__id']

    current_qualification = qualification_model.objects.get(
        id=qualification_id)

    models = get_models(current_qualification)

    for key in row:
        if key == 'qualification__id':
            continue
        key_index, key = parse_key(key)
        if key == 'qualification_entrance_requirement_subject__subject':
            subject_instance, error_subject = set_qualification_entrance_rs(
                row,
                key,
                key_index,
                current_qualification)

            models['qualification_entrance_requirement_subject'] = (
                subject_instance
            )

            errors.update(error_subject)

        elif key == 'interest__name':
            error_interest, dif_interest = set_interest(
                row,
                key,
                key_index,
                current_qualification)

            errors.update(error_interest)


        elif key == 'occupation__name':
            error_occupation, diff_occupation = set_occupation(
                row,
                key,
                key_index,
                current_qualification)

            errors.update(error_occupation)
            diffs[key] = diff_occupation

        else:
            error_generic, diffs[key] = update_key(row, key, key_index, models)
            errors.update(error_generic)

    if len(errors) > 0:
        return False, errors, diffs
    return True, None, diffs


def update_key(row, key, key_index, models):
    errors = {}
    diff = {}
    model_name = key[:key.find(MODEL_DELIMITER)]
    try:
        model = models[model_name]
    except KeyError as e:
        errors[key] = str(e)
    property_name = key[key.find(MODEL_DELIMITER) + len(MODEL_DELIMITER):]
    property_value = row[key]
    if property_value and model:
        try:
            old_value = getattr(model, property_name)
            setattr(model, property_name, property_value)
            model.save()
            diff = {'old': old_value,
                    'new': property_value}
        except Exception as e:
            if key_index > 0:
                errors[f'{key}-{key_index}'] = 'No property value'
            else:
                errors[key] = str(e)

    return errors, diff


def parse_key(key):
    if key.find(ITERATION_DELIMITER) != -1:  # This is a multi column insertion
        key = key[:key.find(ITERATION_DELIMITER)]
        key_index = key[
            key.find(ITERATION_DELIMITER) + len(ITERATION_DELIMITER):]  # noqa
    else:
        key_index = 0
    if type(key_index) != int:
        key_index = 0
    return key_index, key


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


def set_qualification_entrance_rs(
    row,
        key, key_index, current_qualification):
    """
    A subclass for import_excel_cell for getting the appropriate qualification_entrance_requirement_subject object
    :param obj: The excel row object being imported
    :param key: This should be qualification_entrance_requirement_subject__subject
    :param key_index: As received from parse_key(self, key)
    :param current_qualification: The qualification model object
    :return: qualification_entrance_requirement_subject to work with, errors
    """  # noqa

    models_qualification_entrance_requirement_subject = None
    errors = {}
    qualification_entrance_requirement_subject_model = apps.get_model(
        'ford3', 'QualificationEntranceRequirementSubject')
    subject_model = apps.get_model('ford3', 'Subject')
    property_value = row[key]
    if property_value is None:
        errors[f'{key}-{key_index}'] = 'No property value'
        return None, errors

    if subject_model.objects.filter(name=property_value).exists():
        current_subject = subject_model.objects.filter(
            name=property_value)[0]

        row[key] = current_subject.id

        try:
            subject_instance = (
                current_qualification.qualificationentrancerequirementsubject_set.all()[key_index])
        except IndexError:
            subject_instance = (
                qualification_entrance_requirement_subject_model.objects.create(
                    qualification=current_qualification, subject=current_subject))

    else:
        errors[f'{key}-{key_index}'] = (
            f'The subject {property_value} does not exist.'
        )
    return subject_instance, errors


def set_interest(row, key, key_index, current_qualification):
    """
    A subclass for import_excel_cell for adding an interest
    :param obj: The excel row object being imported
    :param key: This should be qualification_entrance_requirement_subject__subject
    :param key_index: As received from parse_key(self, key)
    :param current_qualification: The qualification model object
    :return: errors
    """  # noqa

    errors = {}
    diff = {'old': None,
            'new': None}
    interest_model = apps.get_model('ford3', 'Interest')
    property_value = row[key]
    if property_value is None:
        errors[f'{key}-{key_index}'] = 'No property value'
        return errors

    if interest_model.objects.filter(name=property_value).exists():
        interest = interest_model.objects.filter(name=property_value)[0]
        try:
            existing_interests = list(current_qualification.interests.all().values())
            existing_interests[key_index] = interest
            diff = {'old': existing_interests.name,
                    'new': property_value}
            # We overwrite the old list
            current_qualification.interests.set(existing_interests)
        except IndexError:
            # Nothing was in that slot, we add a new one
            current_qualification.interests.add(interest)
            diff['new'] = property_value
    else:
        errors[f'{key}-{key_index}'] = (
            f'The interest {property_value} does not exist.'
        )

    return errors, diff


def set_occupation(row, key, key_index, current_qualification):
    """
    A subclass for import_excel_cell for adding an occupation
    :param obj: The excel row object being imported
    :param key: This should be qualification_entrance_requirement_subject__subject
    :param key_index: As received from parse_key(self, key)
    :param current_qualification: The qualification model object
    :return: errors
    """  # noqa
    errors = {}
    diff = {'old': None,
            'new': None}
    occupation_model = apps.get_model('ford3', 'Occupation')
    property_value = row[key]
    if property_value is None:
        errors[f'{key}-{key_index}'] = 'No property value'
        return errors, diff

    if occupation_model.objects.filter(name=property_value).exists():
        occupation = occupation_model.objects.filter(name=property_value)[0]
        try:
            existing_occupations = list(current_qualification.occupations.all())
            existing_occupations[key_index] = occupation
            current_qualification.occupations.set(existing_occupations)
            diff = {'old': occupation.name,
                    'new': property_value}
        except IndexError:
            # Nothing was in that slot, we add a new one
            current_qualification.occupations.add(occupation)
            diff['new'] = property_value
    else:
        errors[f'{key}-{key_index}'] = (
            f'The interest {property_value} does not exist.'
        )

    return errors, diff
