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

    @property
    def osci_ctrl(self):
        return self.read('P-0-0028')

    @osci_ctrl.setter
    def osci_ctrl(self, v):
        return self.write(v, 'P-0-0028')

    @property
    def osci_status(self):
        return self.read('P-0-0029')

    @property
    def osci_time_resolution(self):
        return self.read('P-0-0031')

    @osci_time_resolution.setter
    def osci_time_resolution(self, v):
        return self.write(v, 'P-0-0031')

    @property
    def osci_mem_depth(self):
        return self.read('P-0-0032')

    @osci_mem_depth.setter
    def osci_mem_depth(self, v):
        return self.write(v, 'P-0-0032')

    @property
    def osci_signal_choice_list(self):
        return self.read('P-0-0149')

    @property
    def osci_num_valid_values(self):
        return self.read('P-0-0150')

    @property
    def osci_trg_mask(self):
        return self.read('P-0-0025')

    @osci_trg_mask.setter
    def osci_trg_mask(self, v):
        return self.write(v, 'P-0-0025')

    @property
    def osci_trg_signal_choice(self):
        return self.read('P-0-0026')

    @osci_trg_signal_choice.setter
    def osci_trg_signal_choice(self, v):
        return self.write(v, 'P-0-0026')

    @property
    def osci_trg_threshold(self):
        return self.read('P-0-0027')

    @osci_trg_threshold.setter
    def osci_trg_threshold(self, v):
        return self.write(v, 'P-0-0027')

    @property
    def osci_trg_slope(self):
        return self.read('P-0-0030')

    @osci_trg_slope.setter
    def osci_trg_slope(self, v):
        return self.write(v, 'P-0-0030')

    @property
    def osci_num_values_after_trg(self):
        return self.read('P-0-0033')

    @property
    def osci_trg_ctrl_offset(self):
        return self.read('P-0-0035')

    @property
    def osci_external_trigger(self):
        return self.read('P-0-0036')

    @osci_external_trigger.setter
    def osci_external_trigger(self, v):
        return self.write(v, 'P-0-0036')

    @property
    def osci_internal_trigger(self):
        return self.read('P-0-0037')

    @osci_internal_trigger.setter
    def osci_internal_trigger(self, v):
        return self.write(v, 'P-0-0037')


    def read_list(self, type_, set_=None, number=None):
        if set_ is None or number is None:
            p_desc = cmd.type_set_number_from_string(type_)

        b = cmd.read_list(*p_desc)

        self.serial.write(b)
        self.serial.flush()

        time.sleep(2)
        result = self.serial.read(self.serial.inWaiting())

        return result
