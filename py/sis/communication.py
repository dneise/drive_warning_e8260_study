import serial
from . import make_command as cmd
from .response import Response

tf = cmd.TelegramFactory()
IDN = cmd.IDN.from_string


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

    def _receive(self):
        self.serial.flush()
        result = self.serial.read(4)
        if len(result) < 4:
            raise TimeoutError('Drive is probably off')
        length = result[2]
        assert result[2] == result[3]
        result += self.serial.read(length+4)

        return Response(result)

    def read(self, idnstr):
        self.serial.write(tf.read(IDN(idnstr)))
        return self._receive()

    def cancel_tranfer(self):
        self.serial.write(tf.cancel_tranfer())
        return self._receive()

    def read_list(self, idnstr, length, offset=0):
        self.serial.write(tf.read_list(IDN(idnstr), offset, length))
        return self._receive()

    def write(self, idnstr, value, size=2):
        self.serial.write(tf.write(IDN(idnstr), value, size))
        return self._receive()

    def rw(self, idnstr, value=None, size=2):
        if value is None:
            return self.read(idnstr)
        else:
            return self.write(idnstr, value, size)

    def osci_trg_mask(self, v=None):
        return self.rw('P-0-0025', v, 4)
    def osci_trg_signal_choice(self, v=None):
        return self.rw('P-0-0026', v, 4)
    def osci_trg_threshold(self, v=None):
        return self.rw('P-0-0027', v, 4)
    def osci_ctrl(self, v=None):
        return self.rw('P-0-0028', v, 2)
    def osci_trg_slope(self, v=None):
        return self.rw('P-0-0030', v, 2)
    def osci_time_resolution(self, v=None):
        return self.rw('P-0-0031', v, 4)
    def osci_mem_depth(self, v=None):
        return self.rw('P-0-0032', v, 2)
    def osci_external_trigger(self, v=None):
        return self.rw('P-0-0036', v, 2)
    def osci_internal_trigger(self, v=None):
        return self.rw('P-0-0037', v, 2)

    def osci_status(self):
        return self.rw('P-0-0029')
    def osci_num_values_after_trg(self):
        return self.rw('P-0-0033')
    def osci_trg_ctrl_offset(self):
        return self.rw('P-0-0035')
    def osci_signal_choice_list(self):
        return self.rw('P-0-0149')
    def osci_num_valid_values(self):
        return self.rw('P-0-0150')

    def get_osci(self):
        print('ctrl', self.osci_ctrl().value)
        print('status', self.osci_status().value)
        print('time_resolution', self.osci_time_resolution().value)
        print('mem_depth', self.osci_mem_depth().value)
        print('num_valid_values', self.osci_num_valid_values().value)
        print('trigger')
        print('    mask', self.osci_trg_mask().value)
        print('    signal_choice', self.osci_trg_signal_choice().value)
        print('    threshold', self.osci_trg_threshold().value)
        print('    slope', self.osci_trg_slope().value)
        print('    num_values_after_trg', self.osci_num_values_after_trg().value)
        print('    ctrl_offset', self.osci_trg_ctrl_offset().value)
        print('    ext trg', self.osci_external_trigger().value)
        print('    int trg', self.osci_internal_trigger().value)
