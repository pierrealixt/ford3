from rest_framework import serializers
from ford3.models.saqa_qualification import SAQAQualification
from api.serializers.field_of_study import FieldOfStudySerializer
from api.serializers.sub_field_of_study import SubFieldOfStudySerializer


class SAQAQualificationSerializer(serializers.ModelSerializer):
    field_of_study = FieldOfStudySerializer()
    sub_field_of_study = SubFieldOfStudySerializer()
    creator_provider = serializers.StringRelatedField()

    class Meta:
        model = SAQAQualification
        fields = '__all__'
