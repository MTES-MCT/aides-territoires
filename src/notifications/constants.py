NOTIFICATION_TYPES_LIST = [
    ("aid_team", "Notification aide structure"),
    ("aid_user", "Notification aide personnelle"),
    ("internal_team", "Notification interne structure"),
    ("internal_user", "Notification interne personnelle"),
]

NOTIFICATION_TYPES_KEYS = [k[0] for k in NOTIFICATION_TYPES_LIST]

NOTIFICATION_SETTINGS_MODES_LIST = [
    ("none", "Aucune"),
    ("internal_only", "Notification interne uniquement"),
    ("internal_email", "Notification interne et par email"),
]

NOTIFICATION_SETTINGS_FREQUENCIES_LIST = [
    ("daily", "Quotidienne"),
    ("weekly", "Hebdomadaire"),
]