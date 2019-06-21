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


class CompletionAudit():
    def __init__(self, obj, rules):
        self.obj = obj
        self.rules = rules
        self.completion_rate = 0

    def run(self) -> int:
        for rule in self.rules:
            require = True
            if 'require' in rule:
                require = self.eval_expr(self.obj, rule['require'], False)

            value = self.eval_expr(self.obj, rule['prop'], None)
            result = [
                func(value)
                for func in rule['funcs']
                if require
            ]
            if rule['prop'] == 'total_cost':

                print(rule)
                print(result)
                print(value)
            self.completion_rate += False not in result

        return int((self.completion_rate / len(self.rules)) * 100)

    def eval_expr(self, obj, prop, ret_except_val):
        try:
            expr = eval(f'obj.{prop}')
        except:
            expr = ret_except_val
        return expr
