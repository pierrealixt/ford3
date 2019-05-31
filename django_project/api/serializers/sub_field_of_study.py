from rest_framework import serializers
from ford3.models.sub_field_of_study import SubFieldOfStudy
from api.serializers.occupation import OccupationSerializer


class SubFieldOfStudySerializer(serializers.ModelSerializer):
    occupation_id = OccupationSerializer()

    class Meta:
        model = SubFieldOfStudy
        fields = '__all__'
