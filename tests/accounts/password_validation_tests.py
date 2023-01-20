from accounts.validators import validate_password
import pytest

length = 'must be at least 8 characters long'
ony_letter = 'must contain at least 1 digit'
only_number = 'Your password cannot be entirely numeric'

@pytest.mark.parametrize('password, result',(
        ('9206', f'{length}  {only_number}'),
        ('770314967', f'  {only_number}'),
        ('', f'{length} {ony_letter} '),
        ('erdf', f'{length} {ony_letter} '),
        ('rf30311888', '  '),
        ('sdjhfjkddf', f' {ony_letter} '),
        ('6405136657df', '  '),
        ('s4050756899', '  '),
        ('71sdfdmd', '  '),
        ('sdf4', f'{length}  '),
        ('92051df415692', '  '),
))
def test_password_ok(password, result):
    assert validate_password(password) == result