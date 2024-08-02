import pytest
from app.exceptions import InvalidPassword


def test_invalid_password():
    e = InvalidPassword("blah")
    assert isinstance(e, InvalidPassword)

    with pytest.raises(TypeError):
        InvalidPassword()
