# CS4333 Project 2 🛜

The objective of this project was to implement the sliding-window and stop-and-wait algorithms for connectionless UDP file transfer.


## Usage

The receiver should always be started before the sender.

### Stop-and-Wait

**Receive.py**
```python
from core import ReceiveUDP

r = ReceiveUDP()
r.set_filename("abs/path/to/save/to.bin")
r.set_localport(12345) # The port the reciever binds to
r.set_mode(0) # 0 indicates stop-and-wait
r.receive_file()
```


**Send.py**
```python
from core import SendUDP

sender = SendUDP()
sender.set_filename("abs/path/to/file.bin")
sender.set_mode(0) # 0 indicates stop-and-wait
sender.set_localport(8000) # The sender socket binds to this port to receives acks
sender.set_receiver(("127.0.0.1", 12345)) # This is the ip and port of the receiver
s.set_timeout(10000) # timeout in ms
s.send_file() # Initiate sending
```

### Sliding-Window

**Receive.py**
```python
from core import ReceiveUDP

r = RecieveUDP()
r.set_filename("abs/path/to/save/to.bin")
r.set_localport(12346)
r.set_mode(1) # 1 indicates sliding window
r.set_modeparameter(20000) # 20000 is the number of bytes allowed "in flight"
r.receive_file()
```

**Send.py**
```python
s.set_filename("abs/path/to/file.bin")
s.set_mode(1) # 1 indicates sliding window
s.set_modeparameter(20000)
s.set_localport(7000)
s.set_receiver(("127.0.0.1", 12346))
s.set_timeout(10000)
s.send_file()
```
