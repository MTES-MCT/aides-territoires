QUESTION_TYPE_VF = "VF"
QUESTION_TYPE_QCM = "QCM"
QUESTION_TYPE_QCM_RM = "QCM-RM"
QUESTION_TYPE_CHOICES = [
    (QUESTION_TYPE_VF, "Vrai ou Faux"),
    (QUESTION_TYPE_QCM, "Questionnaire à choix multiples"),
    (
        QUESTION_TYPE_QCM_RM,
        "Questionnaire à choix multiples avec réponses multiples",
    ),  # noqa
]

QUESTION_ANSWER_CHOICE_LIST = ["a", "b", "c", "d"]
