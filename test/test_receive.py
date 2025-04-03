'''
Unit tests for core/receive.py
'''
from core.receive import ReceiveUDP


def test_valid_field_updates():
    '''
    Unit test for valid `ReceiveUDP` field updates.
    '''
    r = ReceiveUDP()

    #region setters
    assert r.set_filename("you_can_write_to_any_file.bin")
    assert r.set_localport(12345)
    assert r.set_mode(1)
    assert r.set_modeparameter(512)
    #endregion
    #region getters
    assert r.get_filename() == "you_can_write_to_any_file.bin"
    assert isinstance(r.get_filename(), str)
    assert r.get_localport() == 12345
    assert isinstance(r.get_localport(), int)
    assert r.get_mode() == 1
    assert isinstance(r.get_mode(), int)
    assert r.get_modeparameter() == 512
    assert isinstance(r.get_modeparameter(), int)

def test_invalid_field_updates():
    '''
    Unit test for invalid `ReceiveUDP` field updates.
    '''
    r = ReceiveUDP()
    assert not r.set_localport(-2)
    assert not r.set_mode(2)

def test_no_file_name_receive():
    '''
    Test for not providing a file name and calling `receive_file()`.
    '''

    r = ReceiveUDP()
    assert not r.receive_file()

def test_illegal_mode():
    '''
    Test for illegally setting mode field to an invalid mode.
    '''

    r = ReceiveUDP()
    r.set_filename("some_file.bin")
    r.mode = 2
    assert not r.receive_file()
