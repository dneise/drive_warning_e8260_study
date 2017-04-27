import serial
from . import make_command as cmd


class IndraDrive:

    def __init__(self):
        self.serial = None
        self.known_parameter_sizes = {}

    @classmethod
    def with_serial(cls, *args, **kwargs):
        if 'baudrate' not in kwargs:
            kwargs['baudrate'] = 115200
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 4
        if 'parity' not in kwargs:
            kwargs['parity'] = serial.PARITY_NONE

        inst = cls()
        inst.serial = serial.Serial(*args, **kwargs)
        return inst

    def raw_read(self, type_, set_=None, number=None):
        if set_ is None or number is None:
            p_desc = cmd.type_set_number_from_string(type_)

        b = cmd.read(*p_desc)

        self.serial.write(b)
        self.serial.flush()

        size_ = self.known_parameter_sizes.get(p_desc, None)
        if size_ is not None:
            result = self.serial.read(size_)
            if len(result) != size_:
                raise TimeoutError
        else:
            time.sleep(2)
            result = self.serial.read(self.serial.inWaiting())
            self.known_parameter_sizes[p_desc] = len(result)

        return result

    def read(self, type_, set_=None, number=None):
        result = self.raw_read(type_, set_, number)

        assert sum(result) % 256 == 0  # checksum
