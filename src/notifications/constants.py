NOTIFICATION_TYPES_LIST = [
    ("aid_team", "Notification aide structure"),
    ("aid_user", "Notification aide personnelle"),
    ("generic_team", "Notification générique structure"),
    ("generic_user", "Notification générique personnelle"),
]

NOTIFICATION_TYPES_KEYS = [k[0] for k in NOTIFICATION_TYPES_LIST]

NOTIFICATION_SETTINGS_MODES_LIST = [
    ("none", "Aucune"),
    ("internal_only", "Notification en ligne uniquement"),
    ("internal_email", "Notification en ligne et par email"),
]

NOTIFICATION_SETTINGS_FREQUENCIES_LIST = [
    ("daily", "Quotidienne"),
    ("weekly", "Hebdomadaire"),
]
