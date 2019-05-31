from rest_framework import serializers
from ford3.models.interest import Interest


class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = '__all__'
