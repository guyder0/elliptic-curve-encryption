import pytest
from ec.koblitz import *
from ec.elliptic_curve import EllipticCurve
from ec.named_curves import registered_curves

@pytest.mark.parametrize('message,curve,err',
    [('hello world!', name, False) for name in registered_curves()] +
    [('hello world!' * 10, name, 'Сообщение слишком длинное') for name in registered_curves()]
)
def test_koblitz_method(message, curve, err):
    ec = EllipticCurve(curve)

    if err:
        try:
            koblitz_encoding(ec, message)
            assert not 'требуется срабатывание ошибки'
        except Exception as e:
            assert e.args[0] == err

    else:

        point_from_message = koblitz_encoding(ec, message)
        assert point_from_message.on_curve()

        message_from_point = koblitz_decoding(ec, point_from_message)
        assert message == message_from_point