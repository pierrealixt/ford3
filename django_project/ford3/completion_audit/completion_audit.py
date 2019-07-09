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

            if len(result) > 0:
                self.completion_rate += False not in result

        return int((self.completion_rate / len(self.rules)) * 100)

    def eval_expr(self, obj, prop, ret_except_val):
        try:
            expr = eval(f'obj.{prop}')
        except:
            expr = ret_except_val
        return expr
