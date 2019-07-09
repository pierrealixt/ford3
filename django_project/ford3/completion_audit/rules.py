from ford3.completion_audit.functions import isPresent


QUALIFICATION = [
    {
        'prop': 'short_description',
        'funcs': [isPresent]
    },
    {
        'prop': 'long_description',
        'funcs': [isPresent]
    },
    {
        'prop': 'duration',
        'funcs': [isPresent]
    },
    {
        'prop': 'full_time',
        'funcs': [isPresent]
    },
    {
        'prop': 'credits_after_completion',
        'funcs': [isPresent]
    },
    {
        'prop': 'distance_learning',
        'funcs': [isPresent]
    },
    {
        'prop': 'total_cost',
        'funcs': [isPresent]
    },
    {
        'prop': 'total_cost_comment',
        'funcs': [isPresent]
    },
    {
        'prop': 'critical_skill',
        'funcs': [isPresent]
    },
    {
        'prop': 'green_occupation',
        'funcs': [isPresent]
    },
    {
        'prop': 'high_demand_occupation',
        'funcs': [isPresent]
    },
    {
        'prop': 'requirement.assessment',
        'funcs': [isPresent]
    },
    {
        'prop': 'requirement.assessment_comment',
        'funcs': [isPresent],
        'require': 'requirement.assessment'
    },
    {
        'prop': 'requirement.interview',
        'funcs': [isPresent],
    },
    {
        'prop': 'requirement.admission_point_score',
        'funcs': [isPresent],
    },
    {
        'prop': 'requirement.min_nqf_level',
        'funcs': [isPresent],
    },
    {
        'prop': 'requirement.portfolio',
        'funcs': [isPresent],
    },
    {
        'prop': 'requirement.portfolio_comment',
        'funcs': [isPresent],
        'require': 'requirement.portfolio'
    },
    {
        'prop': 'requirement.require_aps_score',
        'funcs': [isPresent],
    },
    {
        'prop': 'requirement.aps_calculator_link',
        'funcs': [isPresent],
        'require': 'requirement.require_aps_score'
    },
    {
        'prop': 'requirement.require_certain_subjects',
        'funcs': [isPresent]
    },
]

CAMPUS = [
    {
        'prop': 'name',
        'funcs': [isPresent]
    },
    {
        'prop': 'telephone',
        'funcs': [isPresent]
    },
    {
        'prop': 'email',
        'funcs': [isPresent]
    },
    {
        'prop': 'max_students_per_year',
        'funcs': [isPresent]
    },
    {
        'prop': 'physical_address',
        'funcs': [isPresent]
    },
    {
        'prop': 'postal_address',
        'funcs': [isPresent]
    }
]
