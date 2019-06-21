from ford3.completion_audit.functions import isPresent


CAMPUS_COMPLETION_RULES = [
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

QUALIFICATION_COMPLETION_RULES = [
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
        'prop': 'requirement.assesment',
        'funcs': [isPresent]
    }
]


class CompletionAudit():
    def __init__(self, obj, rules):
        self.obj = obj
        self.rules = rules
        self.completion_rate = 0

    def run(self) -> int:
        for rule in self.rules:
            result = [
                func(getattr(self.obj, rule['prop']))
                for func in rule['funcs']
            ]

            self.completion_rate += False not in result

        return int((self.completion_rate / len(self.rules)) * 100)
