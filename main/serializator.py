from rest_framework import serializers
from .models import Question


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "text",
        ]
