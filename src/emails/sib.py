from anymail.message import AnymailMessage


def send_mail_sib_with_template(
        recipient_list, template_id, data=None, tags=None,
        fail_silently=False):
    message = AnymailMessage(to=recipient_list)
    message.template_id = template_id
    if tags:
        message.tags = tags
    message.from_email = None  # use the template's default sender
    if data:
        message.merge_global_data = data
    message.send(fail_silently=fail_silently)
