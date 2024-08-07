from email_validator import validate_email, EmailNotValidError


def validate_email_format(email: str):
    msg = ""
    valid = False
    try:
        email_info = validate_email(email)
        email = email_info.normalized
        valid = True
    except EmailNotValidError as e:
        msg = str(e)
    return valid, msg, email
