from rest_framework import serializers

from eligibility.models import (
    EligibilityTest,
    EligibilityQuestion,
    EligibilityTestQuestion,
)  # noqa


class EligibilityQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityQuestion
        exclude = ("author", "date_created", "date_updated")


class EligibilityTestQuestionSerializer(serializers.ModelSerializer):
    question = EligibilityQuestionSerializer()

    def to_representation(self, obj):
        """Flatten nested 'question' dict."""
        representation = super().to_representation(obj)
        question_representation = representation.pop("question")
        for key in question_representation:
            representation[key] = question_representation[key]
        return representation

    class Meta:
        model = EligibilityTestQuestion
        fields = ("order", "question")


class EligibilityTestSerializer(serializers.ModelSerializer):
    questions = EligibilityTestQuestionSerializer(
        source="eligibilitytestquestion_set", many=True
    )  # noqa

    class Meta:
        model = EligibilityTest
        exclude = ("author", "date_created", "date_updated")
