class QualificationAudit(object):
    PREFIX = 'audit'

    def __init__(self, qualififcation):
        self.qualification = qualififcation

    def evaluate_audit(self):
        return False if False in [
            eval(f'self.{method}()')
            for method in dir(self)
            if self.is_audit_method(method)
        ] else True

    def is_audit_method(self, method):
        return method[0:5] == self.PREFIX

    def audit_short_description(self):
        return self.qualification.short_description is not None \
               and len(self.qualification.short_description) > 0

    def audit_distance_learning(self):
        return self.qualification.distance_learning is not None

    def audit_full_time(self):
        return self.qualification.full_time is not None

    def audit_duration(self):
        return self.qualification.duration is not None

    def audit_min_nqf_level(self):
        try:
            return self.qualification.requirement.min_nqf_level is not None
        except AttributeError:  # Will be raised if there is no requirement
            return False

    def audit_required_subjects(self):
        try:
            if self.qualification.requirement.require_certain_subjects \
                    is not None:
                if self.qualification.requirement.require_certain_subjects:
                    return len(
                        self.qualification.entrance_req_subjects_list) > 0
                else:
                    return True
            else:
                return False
        except AttributeError:  # Will be raised if there is no requirement
            return False

    def audit_occupations(self):
        return len(self.qualification.occupation_name_list) > 0
