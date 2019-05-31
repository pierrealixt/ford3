from rest_framework import serializers
from ford3.models.occupation import Occupation


class OccupationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Occupation
        fields = '__all__'
