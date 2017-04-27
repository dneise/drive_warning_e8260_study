import serial
from . import make_command as cmd
import time
import struct


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

        time.sleep(0.5)
        result = self.serial.read(self.serial.inWaiting())

        return result

    def read(self, type_, set_=None, number=None):
        result = self.raw_read(type_, set_, number)

        cmd.check_response(result)
        print('status:', cmd.get_status(result))
        print('service:', cmd.get_service(result))

        L = len(result) - 11
        if L == 2:
            num = struct.unpack('<h', result[11:])[0]
        elif L == 4:
            num = struct.unpack('<i', result[11:])[0]
        else:
            num = None

        return num, result

    def write(self, value, type_, set_=None, number=None, size=2):
        if set_ is None or number is None:
            type_, set_, number = cmd.type_set_number_from_string(type_)

        b = cmd.write(type_, set_, number, value, size)

        self.serial.write(b)
        self.serial.flush()

        time.sleep(1)
        result = self.serial.read(self.serial.inWaiting())

        cmd.check_response(result)
        print('status:', cmd.get_status(result))
        print('service:', cmd.get_service(result))

        L = len(result) - 11
        if L == 2:
            num = struct.unpack('<h', result[11:])[0]
        elif L == 4:
            num = struct.unpack('<i', result[11:])[0]
        else:
            num = None
        if num in cmd.fehlercodes:
            print('fehlercode:', cmd.fehlercodes[num])

        return num, result

    def osci_ctrl(self, v=None):
        if value is None:
            return self.read('P-0-0028')
        else:
            return self.write(v, 'P-0-0028')

    def osci_status(self):
        return self.read('P-0-0029')

    def osci_time_resolution(self, v=None):
        if v is None:
            return self.read('P-0-0031')
        else:
            return self.write(v, 'P-0-0031', size=4)

    def osci_mem_depth(self, v=None):
        if v is None:
            return self.read('P-0-0032')
        else:
            return self.write(v, 'P-0-032', size=4)

    def osci_signal_choice_list(self):
        return self.read('P-0-0149')

    def osci_num_valid_values(self):
        return self.read('P-0-0150')

    def osci_trg_mask(self, v=None):
        if v is None:
            return self.read('P-0-0025')
        else:
            return self.write(v, 'P-0-0025', size=4)

    def osci_trg_signal_choice(self, v=None):
        if v is None:
            return self.read('P-0-0026')
        else:
            return self.write(v, 'P-0-0026', size=4)

    def osci_trg_threshold(self, v=None):
        if v is None:
            return self.read('P-0-0027')
        else:
            return self.write(v, 'P-0-0027', size=4)

    def osci_trg_slope(self, v=None):
        if v is None:
            return self.read('P-0-0030')
        else:
            return self.write(v, 'P-0-0030', size=2)

    def osci_num_values_after_trg(self):
        return self.read('P-0-0033')

    def osci_trg_ctrl_offset(self):
        return self.read('P-0-0035')

    def osci_external_trigger(self, v=None):
        if v is None:
            return self.read('P-0-0036')
        else:
            return self.write(v, 'P-0-0036', size=2)

    def osci_internal_trigger(self, v=None):
        if v is None:
            return self.read('P-0-0037')
        else:
            return self.write(v, 'P-0-0037', size=2)

    def get_osci(self):
        print('ctrl', self.osci_ctrl()[0])
        print('status', hex(self.osci_status()[0]))
        print('time_resolution', self.osci_time_resolution()[0])
        print('mem_depth', self.osci_mem_depth()[0])
        print('num_valid_values', self.osci_num_valid_values()[0])
        print('trigger')
        print('    mask', self.osci_trg_mask()[0])
        print('    signal_choice', hex(self.osci_trg_signal_choice()[0]))
        print('    threshold', self.osci_trg_threshold()[0])
        print('    slope', self.osci_trg_slope()[0])
        print('    num_values_after_trg', self.osci_num_values_after_trg()[0])
        print('    ctrl_offset', self.osci_trg_ctrl_offset()[0])
        print('    ext trg', self.osci_external_trigger()[0])
        print('    int trg', self.osci_internal_trigger()[0])


    def read_list(self, type_, length=100, set_=None, number=None):
        if set_ is None or number is None:
            p_desc = cmd.type_set_number_from_string(type_)

        b = cmd.read_list(
            p_desc[0],
            p_desc[1],
            p_desc[2],
            0,
            length
        )

        self.serial.write(b)
        self.serial.flush()

        time.sleep(2)
        result = self.serial.read(self.serial.inWaiting())

        cmd.check_response(result)
        print('status:', cmd.get_status(resulazt))
        print('service:', cmd.get_service(result))
        return result
