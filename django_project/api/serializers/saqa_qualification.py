from rest_framework import serializers
from ford3.models.saqa_qualification import SAQAQualification


class SAQAQualificationSerializer(serializers.ModelSerializer):

    field_of_study = serializers.StringRelatedField()
    sub_field_of_study = serializers.StringRelatedField()

    class Meta:
        model = SAQAQualification
        exclude = ['id', 'creator_provider', 'nqf_level']
