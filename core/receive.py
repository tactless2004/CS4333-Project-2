'''
receive is a class for receiving UDP datagrams.
'''
import os
from socket import socket, AF_INET as ipv4, SOCK_DGRAM as connectionless, inet_ntoa as decode_ip
class ReceiveUDP:
    '''
    ReceiveUDP is an interface for receiving files over UDP.
    '''
    def __init__(self):
        self._mtu = 1500  # TODO: make toml config file and make this changeable there.
        self.file_name = str()
        self.local_port = int()
        self.mode = int()
        self.mode_parameter = int()

    #region getters
    def get_filename(self):
        '''
        Getter method for file_name field.
        '''
        return self.file_name

    def get_localport(self):
        '''
        Getter method for local_port field.
        '''
        return self.local_port

    def get_mode(self):
        '''
        Getter method for mode field.
        '''
        return self.mode

    def get_modeparameter(self):
        '''
        Getter method for mode_parameter field.
        '''
        return self.mode_parameter
    #endregion
    #region setters
    def set_filename(self, filename: str) -> bool:
        '''
        Setter method for filename field.

        :param filename: symbolic link of the intended transfer file
        :raises AssertionError: filename must exist on the sending machine
        '''

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

        self.mode = mode
        return True

    def set_modeparameter(self, mode_parameter: int) -> bool:
        '''
        Setter method for mode_parameter field.

        :param mode_parameter: mode_parameter is an optional field used by some modes
        '''
        self. mode_parameter = mode_parameter
        return True
    #endregion
    #region recv
    def receive_file(self):
        '''
        Receive a file over UDP.
        '''
        # Never set filename
        if self.get_filename() == "":
            return False

        if self.get_mode() == 0:
            return self._receive_stw()
        if self.get_mode() == 1:
            return self._receive_sw()

        print("FART")
        return False

    def _receive_stw(self):
        receive = socket(ipv4, connectionless)
        receive.bind(("localhost", self.get_localport()))
        receive.settimeout(10.0)
        recv = True
        data = {}
        while recv:
            # 1. Get Data
            datum, _ = receive.recvfrom(self._mtu)

            # 2. Strip header values
            packet_count = int.from_bytes(datum[0:2])
            packet_no = int.from_bytes(datum[2:4])
            ip_addr = decode_ip(datum[4:8])
            port = int.from_bytes(datum[8:10])
            datum = datum[10:]

            # 3. Write data
            data[packet_no] = datum

            # 4. Acket the packet
            receive.sendto(int(255).to_bytes(), (ip_addr, port))

            # 5. Is this the last packet? Yes -> write_data, exit; No -> get next packet
            if packet_no >= packet_count:
                recv = False

        return self._write_data(data)

    def _receive_sw(self) -> bool:
        pass

    def _write_data(self, data: dict) -> bool:
        datum_count = len(data.keys())
        data = "".join([data[x].decode("ascii") for x in range(1, datum_count+1)])
        with open(self.get_filename(), "w", encoding = "ascii") as f:
            f.write(data)

        return True
    #endregion
