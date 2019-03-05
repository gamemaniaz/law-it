from rest_framework import serializers
from chatmiddleware.models import Lawyer

class LawyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lawyer
        fields = ('id', 'name', 'job_title', 'key_practice_areas', 'law_prac_name', 'law_prac_type', 'email', 'website', 'tel', 'address', 'cases', 'disciplinary_fault')

class AOLSerializer(serializers.Serializer):
    aol_keywords = serializers.CharField(required=True, allow_blank=False, max_length=100)
    intent_keywords = serializers.CharField(required=True, allow_blank=False, max_length=100)

class LanguageSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, allow_blank=False)
