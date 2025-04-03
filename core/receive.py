# pylint: disable=duplicate-code
'''
`receive` is a class for receiving UDP datagrams.
'''
import tomllib
from socket import(
    socket, AF_INET as ipv4,
    SOCK_DGRAM as connectionless,
    inet_ntoa as decode_ip,
    timeout  # socket.timeout exception
)
from threading import Thread
class ReceiveUDP:
    '''
    ReceiveUDP is an interface for receiving files over UDP.
    '''
    def __init__(self):
        with open("config.toml", "r", encoding="utf-8") as f:
            self.config = tomllib.loads(f.read())
        self.file_name = str()
        self.local_port = int()
        self.mode = 0
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
        if port < 0 or port > 65535:
            return False

        self.local_port = port
        return True

    def set_mode(self, mode: int) -> bool:
        '''
        Setter method for mode field.

        :param mode: 0 indiciates stop-and-wait; 1 indiciates sliding window
        '''
        if not mode in [0, 1]:
            return False

        self.mode = mode
        return True

    def set_modeparameter(self, mode_parameter: int) -> bool:
        '''
        Setter method for mode_parameter field.

        :param mode_parameter: mode_parameter is an optional field used by some modes
        '''
        self.mode_parameter = mode_parameter
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
        return False

    def _receive_stw(self):
        receive = socket(ipv4, connectionless)
        receive.bind(("localhost", self.get_localport()))
        receive.settimeout(10.0)
        recv = True
        data = {}
        while recv:
            # 1. Get Data
            datum, _ = receive.recvfrom(self.config['mtu'])

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
        recv = socket(ipv4, connectionless)
        recv.bind(('localhost', self.get_localport()))
        recv.settimeout(0.2)

        received = {
            'inited' : False,
            'packet_count' : int(),
            'to_ack' : [],
            'sender' : tuple[str, int],
            'acked' : 0
        }
        ack_thread = Thread(target = self._ack_sender, args = (received,))
        ack_thread.start()

        data = {}


        receiving = True
        first_receive = True
        packet_count = 0
        while receiving:
            if first_receive:
                try:
                    # Receive the first data packet
                    datum, _ = recv.recvfrom(self.config['mtu'])
                    # Parse the packet out
                    packet_count = int.from_bytes(datum[0:2])
                    packet_no = int.from_bytes(datum[2:4])
                    ip_addr = decode_ip(datum[4:8])
                    port = int.from_bytes(datum[8:10])
                    data[packet_no] = datum[10:]

                    # Set 'env variables'
                    # received['packet_count'] tells _ack_sender() when its acked all packets
                    # this variable should be considered READONLY.
                    received['packet_count'] = packet_count
                    received['sender'] = (ip_addr, port)
                    received['to_ack'].append(packet_no)
                    received['inited'] = True

                    # Now do normal receive
                    first_receive = False

                    packet_count -= 1
                    if received['packet_count'] == 1:
                        break
                except timeout:
                    continue
            try:
                datum, _ = recv.recvfrom(self.config['mtu'])
                packet_no = int.from_bytes(datum[2:4])
                data[packet_no] = datum[10:]
                received['to_ack'].append(packet_no)
                packet_count -= 1
                receiving = packet_count > 0
            except timeout:
                continue
        ack_thread.join()
        assert received['acked'] == received['packet_count']
        return self._write_data(data)

    def _write_data(self, data: dict) -> bool:
        datum_count = len(data.keys())
        data = b"".join([data[x] for x in range(1, datum_count+1)])
        with open(self.get_filename(), "wb") as f:
            f.write(data)

        return True

    def _build_ack(self, ack_num: int) -> bytes:
        return bytes(int(255).to_bytes() + ack_num.to_bytes(length = 2))

    def _ack_sender(self, received: dict):
        while not received['inited']:
            continue

        sender = socket(ipv4, connectionless)
        acking = True

        while acking:
            if received['to_ack'] != []:
                ack_num = received['to_ack'].pop(0)
                sender.sendto(
                    self._build_ack(ack_num),
                    received['sender']
                )
                received['acked'] += 1
            acking = received['acked'] < received['packet_count']
        sender.close()

    #endregion
