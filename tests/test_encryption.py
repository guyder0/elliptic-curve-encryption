import pytest, os
from ec.encryption import *
from ec.named_curves import registered_curves


@pytest.mark.parametrize('name,passphrase',
                         [(name, passphrase)
                          for name in registered_curves()
                          for passphrase in ['password', 'incorrect']])
def test_key_pairs(name, passphrase):
    ecc_interface = ECC_encryption(name)
    ecc_interface.generate_key_pair('password', 'tmp1', 'tmp2')

    try:
        ecc_interface.select_public_key('tmp2')
        assert not (ecc_interface.public_key is None)
        ecc_interface.select_private_key(passphrase, 'tmp1')
        assert passphrase != 'incorrect'
    except Exception as e:
        assert passphrase == 'incorrect' and e.args[0] == 'Неверная парольная фраза'

    os.remove('tmp1'); os.remove('tmp2')


@pytest.mark.parametrize('name,message',
                         [(name, message)
                          for name in registered_curves()
                          for message in ['msg1', 'fgsfsdfdff' * 40]])
def test_encrypt_decrypt_system(name, message):
    with open('tmp_open_msg', 'w+') as f: f.write(message)
    ecc_interface = ECC_encryption(name)

    ecc_interface.generate_key_pair('PASSWORD', 'tmp_sk', 'tmp_pk')
    ecc_interface.select_private_key('PASSWORD', 'tmp_sk')
    ecc_interface.select_public_key('tmp_pk')

    ecc_interface.encrypt_message('tmp_open_msg', 'tmp_closed_msg')
    ecc_interface.decrypt_message('tmp_closed_msg', 'tmp_final')

    with open('tmp_final', 'r') as f: msg = f.read()
    assert message == msg

    for filename in ['tmp_open_msg', 'tmp_closed_msg', 'tmp_final', 'tmp_sk', 'tmp_pk']:
        os.remove(filename)