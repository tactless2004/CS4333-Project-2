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
        # This is our sender and receiver
        sender = socket(ipv4, connectionless)
        
        # socket.settimeout(timeout: float) takes its time out in seconds, so we convert
        _timeout = float(self.timeout * 1e-3)  # milliseconds -> seconds
        sender.settimeout(_timeout)


        sender.bind(("localhost", self.get_localport()))

        # This is info to transmit in the header to the receiver.
        # Theoretically, the receiver knows the sender's ip by virtue of receiving the packet,
        # so we don't need this.
        listening_ip = sender.getsockname()[0]  # (ip_addr, port)[0] = ip_addr
        listening_port = self.get_localport()

        with open(self.get_filename(), "rb") as f:
            # Windows '\r\n' line carriage return gets read by python as two new lines... for some reason.
            # So, we just replace \r\n with \n
            data = f.read().replace(bytes("\r\n", encoding = "ascii"), bytes("\n", encoding = "ascii"))

        packet_size = self._mtu - self._header_size
        # Turn the data into `packet_size`d slices for transmission.
        # This code will need to be modified if we choose a different encoding than ASCII
        data = [data[x: x + packet_size] for x in range(0, len(data), packet_size)]
        packet_count = len(data)

        for i, datum in enumerate(data, start = 1):
            print(f"Message {i} sent with {packet_size} bytes of actual data")
            sender.sendto(
                self._make_header(i, packet_count, listening_ip, listening_port) + datum, # data
                self.get_receiver()                                                       # adress
            )
            # Can play with this sleep value, to try and get faster sends.
            sleep(0.01)
            try:
                # If this doesn't receive an ack IMMEDIATELY, it will throw WinError [10035].
                # Need to find a way to actually enforce the timeout in this case.
                data, _ = sender.recvfrom(self._mtu)
                if self._check_ack(data):
                    print(f"Message {i} acknowledged")
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
