from nose import with_setup
from APUtils import APCrypto, APUtilCF, APUtilFile, APUtilLog, APUtilMath, APUtilStr, APUtilXml, APPageProducer, APUtilSendMail

def setup():
    """
    Setup.
    :return: None.
    """
    pass


def teardown():
    """
    Teardown.
    :return: None.
    """
    pass

@with_setup(setup, teardown)
def test_APCrypto():
    """Test Encript an decrypt
       :return: None.
    """
    SecretPhrase = "Python Is Awesome !!!"
    MyPassword = 'P4ssw0rd'

    enc_result = APCrypto.APEncryptPassword(SecretPhrase, MyPassword)
    assert enc_result == 'J8OiKEdKw5ojNA=='

    dec_result = APCrypto.APDecryptPassword(SecretPhrase, enc_result)
    assert dec_result == 'P4ssw0rd'
