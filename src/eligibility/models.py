from django.db import models
from django.utils import timezone

from eligibility import constants


class EligibilityTest(models.Model):
    """Represents an elibility test."""

    name = models.CharField("Nom", max_length=256)

    introduction = models.TextField("Une introduction", blank=True)
    conclusion_success = models.TextField(
        "Une conclusion si le test est positif", blank=True
    )
    conclusion_failure = models.TextField(
        "Une conclusion si le test est négatif", blank=True
    )
    conclusion = models.TextField("Une conclusion générale", blank=True)

    questions = models.ManyToManyField(
        "EligibilityQuestion",
        through="EligibilityTestQuestion",
        verbose_name="Questions",
        related_name="eligibility_tests",
        blank=True,
    )

    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        verbose_name="Auteur",
        related_name="eligibility_tests",
        null=True,
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Test d’éligibilité"
        verbose_name_plural = "Tests d’éligibilité"

    def __str__(self):
        return self.name


class EligibilityQuestion(models.Model):
    """Represents an elibility question."""

    text = models.TextField("La question")

    answer_choice_a = models.CharField("Réponse A", max_length=256)
    answer_choice_b = models.CharField("Réponse B", max_length=256)
    answer_choice_c = models.CharField("Réponse C", max_length=256, blank=True)
    answer_choice_d = models.CharField("Réponse D", max_length=256, blank=True)
    answer_correct = models.CharField(
        "La bonne réponse",
        max_length=50,
        choices=zip(
            constants.QUESTION_ANSWER_CHOICE_LIST,
            constants.QUESTION_ANSWER_CHOICE_LIST,
        ),
    )

    author = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        verbose_name="Auteur",
        related_name="eligibility_questions",
        null=True,
    )

    date_created = models.DateTimeField("Date de création", default=timezone.now)
    date_updated = models.DateTimeField("Date de mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.text} ({self.answer_correct_value()})"

    def answer_correct_value(self):
        return getattr(self, f"answer_choice_{self.answer_correct}")


class EligibilityTestQuestion(models.Model):
    test = models.ForeignKey("EligibilityTest", on_delete=models.CASCADE)
    question = models.ForeignKey("EligibilityQuestion", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(blank=True, default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.test.name} : {self.question.text}"
