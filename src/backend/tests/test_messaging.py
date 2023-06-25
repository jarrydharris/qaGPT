import pytest
from src.backend.service.messaging import decode_message
from src.backend.service.messaging import validate_message


def test_decoding_user_message_returns_json():
    message = b'{"message":"hi"}'
    assert decode_message(message) == {"message": "hi"}


def test_validate_message_valid_value():
    good_message = "hi"
    assert validate_message(good_message) is True


def test_validate_message_empty_value():
    empty_message = ""
    with pytest.raises(ValueError) as e:
        validate_message(empty_message)
    assert str(e.value) == "The message is an empty string."


def test_validate_message_null_value():
    null_message = None
    with pytest.raises(ValueError) as e:
        validate_message(null_message)
    assert str(e.value) == "Null message."


def test_validate_message_wrong_type():
    num_message = 7
    with pytest.raises(TypeError) as e:
        validate_message(num_message)
    assert str(e.value) == "The value for message is '<class 'int'>' is not a string."
