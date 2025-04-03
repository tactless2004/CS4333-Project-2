# pylint: disable=duplicate-code
'''
Unit test for the Sliding Window algorithm
'''
import os
import hashlib
from multiprocessing import Pool
from core import SendUDP
from core import ReceiveUDP

def test_stop_and_wait():
    '''
    Sliding Window algorithm test using `SendUDP` and `ReceiveUDP`.
    '''
    s = SendUDP()
    r = ReceiveUDP()

    #region init sender
    s.set_filename(os.path.join(os.getcwd(), "test_files", "1mb.bin"))
    s.set_mode(1)
    s.set_modeparameter(20000)
    s.set_localport(7000)
    s.set_receiver(("127.0.0.1", 12346))
    s.set_timeout(10000)
    #endregion
    #region init receiver
    r.set_filename(os.path.join(os.getcwd(), "test_files", "1mb_copy.bin"))
    r.set_localport(12346)
    r.set_mode(1)
    r.set_modeparameter(20000)
    #endregion
    #region test
    with Pool() as pool:
        results = [
            pool.apply_async(r.receive_file),
            pool.apply_async(s.send_file)
        ]
        pool.close()
        pool.join()
    for result in results:
        assert result.get()

    hasher1 = hashlib.new("sha256")
    hasher2 = hashlib.new("sha256")

    with open(os.path.join(os.getcwd(), "test_files", "1mb.bin"), "rb") as f:
        hasher1.update(f.read())
        hash1 = hasher1.hexdigest()

    with open(os.path.join(os.getcwd(), "test_files", "1mb_copy.bin"), "rb") as f:
        hasher2.update(f.read())
        hash2 = hasher2.hexdigest()

    assert hash1 == hash2
    #endregion
