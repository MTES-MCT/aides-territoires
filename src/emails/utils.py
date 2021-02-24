from anymail.message import AnymailMessage


def send_template_email(
        recipient_list, template_id, data=None, tags=None,
        fail_silently=False):
    """Use the "template" feature provided by our ESP"""
    message = AnymailMessage(to=recipient_list)
    message.template_id = template_id
    message.from_email = None  # use the template's default sender

    # Tags can then be found and filtered in the ESP's analytics dashboard
    if tags:
        message.tags = tags

    # Provide data for template replacements
    if data:
        # Currently working with Sendinblue
        message.merge_global_data = data

    message.send(fail_silently=fail_silently)
