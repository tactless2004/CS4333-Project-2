'''
`send` is a module for sending UDP Datagrams.
'''
from socket import socket, AF_INET as ipv4, SOCK_DGRAM as connectionless, timeout
import os
class SendUDP:
    # TODO: Write a concise description.
    '''
    Docstring to make the linter stop complaining
    '''
    # TODO: Does it make sense to have overloads for different parameter combinations?
    def __init__(self):
        # TODO: Add sensible defaults.
        self._mtu = 200  # TODO: make toml config file and make this changeable there.
        self._header_size = 0  # TODO: Add this to config file
        self.file_name = str()
        self.local_port = int()
        self.mode = int()
        self.mode_parameter = int()
        self.timeout = int()
        self.receiver = tuple[str, int]  # (ip_addr, port)

    # Doing getters and setter to confrom to the project specifications,
    # I recognize python doesn't support private object fields nor standard encapsulation,
    # and thus doesn't require getters and setters.

    #region getters
    def get_filename(self) -> str:
        '''
        Getter method for filename field.
        '''
        return self.file_name

    def get_localport(self) -> int:
        '''
        Getter method for local_port field.
        '''
        return self.local_port

    def get_mode(self) -> int:
        '''
        Getter method for local_port field.
        '''
        return self.mode

    def get_modeparameter(self) -> int:
        '''
        Getter method for mode_parameter field.
        '''
        return self.mode_parameter

    def get_receiver(self) -> tuple[str, int]:
        '''
        Getter method for get_receiver field.
        '''
        return self.receiver

    def get_timeout(self) -> int:
        '''
        Getter method for timeout field.
        '''
        return self.timeout

    #endregion
    #region setters
    def set_filename(self, filename: str) -> bool:
        '''
        Setter method for filename field.

        :param filename: symbolic link of the intended transfer file
        :raises AssertionError: filename must exist on the sending machine
        '''
        if not os.path.exists(filename):
            return False

        self.file_name = filename
        return True

    def set_localport(self, port: int) -> bool:
        '''
        Setter method for local_port field.

        :param port: Port for the local machine to bind to
        '''
        self.local_port = port
        return True

    def set_mode(self, mode: int) -> bool:
        '''
        Setter method for mode field.

        :param mode: 0 indiciates stop-and-wait; 1 indiciates sliding window
        '''
        if not mode in [0,1]:
            return False

        self.mode = mode
        return True

    def set_modeparameter(self, mode_parameter: int) -> bool:
        '''
        Setter method for mode_parameter field.

        :param mode_parameter: mode_parameter is an optional field used by some modes
        '''
        self. mode_parameter = mode_parameter
        return True

    def set_receiver(self, receiver: tuple[str, int]) -> bool:
        '''
        Setter method for receiver field.

        :param receiver: (ip_address, port) tuple for socket connection
        '''
        self.receiver = receiver
        return True

    def set_timeout(self, time_out: int) -> bool:
        '''
        Setter method for timeout field.

        :param timeout: time in milliseconds before operations should be considered failed
        '''
        self.timeout = time_out
        return True
    #endregion

    #region core functionality
    def send_file(self) -> bool:
        '''
        Send a `file_name` to `receiver` using a UDP socket
        '''
        if self.get_receiver() == tuple[str, int]:
            return False

        if self.get_mode() == 0:
            self._send_file_stw()
        elif self.get_mode() == 1:
            self._send_file_sw()
        else:
            return False

    def _send_file_stw(self):
        _timeout = float(self.timeout * 1e-3)  # milliseconds -> seconds
        sender = socket(ipv4, connectionless)
        sender.settimeout(_timeout)
        with open(self.get_filename()) as f:
            data = f.read("")
        packet_size = 
        try:
            sender.sendto(b'TEST', self.get_receiver())
        # TODO: Figure out exceptions that this throws and catch them.
        except timeout:
            sender.close()
            print("Send request timed out.")
            return False
        except OSError as e:
            sender.close()
            print(e)
            return False
        except Exception as e:
            sender.close()
            print(e)
            return False
        return True

    def _send_file_sw(self):
        pass
