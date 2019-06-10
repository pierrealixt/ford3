from rest_framework import serializers
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel


class EnumField(serializers.ChoiceField):
    def __init__(self, enum, **kwargs):
        self.enum = enum
        kwargs['choices'] = [(e.name, e.value) for e in enum]
        super(EnumField, self).__init__(**kwargs)

    def to_representation(self, obj):
        if obj != '':
            # obj looks like SaqaQualification.LEVEL_4
            # The split isolates the LEVEL4
            result = SaqaQualificationLevel[obj.split('.', 1)[1]].value
        else:
            result = ''
        return result
