from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_password(password):
    length = ''
    ony_letter = ''
    only_number = ''
    if len(password) < 8:
        length = _('must be at least 8 characters long')
    if any(i.isdigit() for i in password) is False:
        ony_letter = _('must contain at least 1 digit')
    if password.isdecimal():
        only_number = _('Your password cannot be entirely numeric')
    return f'{length} {ony_letter} {only_number}'