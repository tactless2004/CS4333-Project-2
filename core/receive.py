'''
receive is a class for receiving UDP datagrams.
'''
import os
class ReceiveUDP:
    '''
    ReceiveUDP is an interface for receiving files over UDP.
    '''
    def __init__(self):
        self._mtu = 200  # TODO: make toml config file and make this changeable there.
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
        return self.local_port

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
    #endregion
