'''
`send` is a module for sending UDP Datagrams.
'''
from socket import socket, AF_INET as ipv4, SOCK_DGRAM as connectionless, timeout, inet_aton
import os
from time import sleep
class SendUDP:
    # TODO: Write a concise description.
    '''
    Docstring to make the linter stop complaining
    '''
    # TODO: Does it make sense to have overloads for different parameter combinations?
    def __init__(self):
        # TODO: Add sensible defaults.
        self._mtu = 1500  # TODO: make toml config file and make this changeable there.
        self._header_size = 10  # TODO: Add this to config file
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
    #region UDP
    def send_file(self) -> bool:
        '''
        Send a `file_name` to `receiver` using a UDP socket
        '''
        if self.get_receiver() == tuple[str, int]:
            return False

        if self.get_mode() == 0:
            return self._send_file_stw()
        elif self.get_mode() == 1:
            return self._send_file_sw()
        else:
            return False

    def _send_file_stw(self) -> bool:
        _timeout = float(self.timeout * 1e-3)  # milliseconds -> seconds
        sender = socket(ipv4, connectionless)
        listening_ip = '127.0.0.1'
        listening_port = self.get_localport()
        sender.bind(("localhost", self.get_localport()))
        sender.settimeout(_timeout)

        with open(self.get_filename(), "rb") as f:
            data = f.read()

        packet_size = self._mtu - self._header_size
        data = [data[x: x + packet_size] for x in range(0, len(data), packet_size)]
        packet_count = len(data)

        for i, datum in enumerate(data, start = 1):
            print(f"sending {packet_size}B of actual data.")
            sender.sendto(self._make_header(i, packet_count, listening_ip, listening_port) + datum, self.get_receiver())
            sleep(0.2)
            try:
                data, _ = sender.recvfrom(self._mtu)
                if self._check_ack(data):
                    print("Received Acknowledgement!")
                    continue
            except timeout:
                sender.close()
                return False
            except OSError:
                print("There are no valid receivers to receive this data exitting...")
                sender.close()
                return False
            except Exception as e:
                print(f"{e}")
                sender.close()
                return False
            
        return True


    def _send_file_sw(self) -> bool:
        return False

    def _make_header(self, packet_number: int, packet_count: int, listening_ip: str, listening_port: int) -> bytes:
        packet_number = packet_number.to_bytes(length = 2, signed = False)
        packet_count = packet_count.to_bytes(length = 2, signed = False)
        listening_ip = inet_aton(listening_ip)
        listening_port = listening_port.to_bytes(length = 2, signed = False)
        return packet_count + packet_number + listening_ip + listening_port
    
    def _check_ack(self, packet) -> bool:
        if int.from_bytes(packet[0:4]) == 255:
            return True
        return False

    #endregion
