'''
Unit tests for core/send.py
'''
import os
from core.send import SendUDP

def test_valid_field_updates():
    '''
    Unit test for valid `SendUDP` field updates.
    '''
    s = SendUDP()
    #region setters
    assert s.set_filename(os.path.join(os.getcwd(),"test_files","test.txt"))
    assert s.set_localport(12345)
    assert s.set_mode(1)
    assert s.set_modeparameter(512)
    assert s.set_receiver(("127.0.0.1", 12345))
    assert s.set_timeout(10000)
    #endregion
    #region getters
    assert s.get_filename() == os.path.join(os.getcwd(),"test_files","test.txt")
    assert isinstance(s.get_filename(), str)
    assert s.get_localport() == 12345
    assert isinstance(s.get_localport(), int)
    assert s.get_mode() == 1
    assert isinstance(s.get_mode(), int)
    assert s.get_modeparameter() == 512
    assert isinstance(s.get_modeparameter(), int)
    assert s.get_receiver() == ("127.0.0.1", 12345)
    assert isinstance(s.get_receiver(), tuple)
    assert s.get_timeout() == 10000
    assert isinstance(s.get_timeout(), int)
    #endregion
def test_invalid_field_updates():
    '''
    Unit tests for illegal `SendUDP` field updates.
    '''
    s = SendUDP()
    assert not s.set_filename("thisfileDNE.bin")
    assert not s.set_localport(-3)
    assert not s.set_localport(100000)
    assert not s.set_mode(2)
