import struct
from .idn import IDN
from .lookup import simple_services

class Access:
    INACTIVE = 0b000 << 3
    IDN = 0b001 << 3
    NAME = 0b010 << 3
    ATTRIBUTE = 0b011 << 3
    UNIT = 0b100 << 3
    MIN_VALUE = 0b101 << 3
    MAX_VALUE = 0b110 << 3
    VALUE = 0b111 << 3


def make_telegram_head_ctrl_byte(
    number_of_dynamic_subadresses=0,
    has_paket_number=False,
    is_reaction_telegram=False,
        ):
    ctrl_byte = 0x00
    ctrl_byte |= (number_of_dynamic_subadresses & 0x03)
    ctrl_byte |= int(has_paket_number) << 3
    ctrl_byte |= int(is_reaction_telegram) << 4
    return ctrl_byte


def fill_length_into_static_telegram_header(b):
    L = len(b)
    b[2] = L - 8
    b[3] = L - 8
    return b


def fill_checksum_into_static_telegram_header(b):
    b[1] = (-1 * sum(b)) & 0xFF
    assert (sum(b) & 0xFF) == 0
    return b


class TelegramFactory:
    STX = 0x02

    def __init__(self, sender=100, receiver=128):
        self.sender_address = sender
        self.receiver_address = receiver

    def _telegram_header_static(self, service_name):
        return bytearray([
            self.STX,
            0x00,   # checksum, to be filled later
            0x00,   # length, to be filled later
            0x00,   # length repetition
            make_telegram_head_ctrl_byte(
                number_of_dynamic_subadresses=0,
                has_paket_number=False,
                is_reaction_telegram=False,
            ),
            simple_services[service_name],
            self.sender_address,
            self.receiver_address,
        ])

    def _payload_head(self, idn, acc, is_last_transmission=True):
        return bytearray([
            (acc | int(is_last_transmission) << 2),
            self.receiver_address,
            0x00,  # should be static like this
        ]) + bytearray(bytes(idn))

    def read(self, idn):
        b = self._telegram_header_static('Parameter lesen')
        b += self._payload_head(idn, Access.VALUE)

        b = fill_length_into_static_telegram_header(b)
        b = fill_checksum_into_static_telegram_header(b)

        return b

    def attribute(self, idn):
        b = self._telegram_header_static('Parameter lesen')
        b += self._payload_head(idn, Access.ATTRIBUTE)

        b = fill_length_into_static_telegram_header(b)
        b = fill_checksum_into_static_telegram_header(b)

        return b

    def write(self, idn, value, size=2):
        b = self._telegram_header_static('Parameter schreiben')
        b += self._payload_head(idn, Access.VALUE)

        if size == 2:
            b += bytearray(struct.pack('<h', value))
        elif size == 4:
            b += bytearray(struct.pack('<i', value))

        b = fill_length_into_static_telegram_header(b)
        b = fill_checksum_into_static_telegram_header(b)

        return b

    def cancel_tranfer(self):
        b = self._telegram_header_static('Abbruch der Datenübertragung')
        b = fill_length_into_static_telegram_header(b)
        b = fill_checksum_into_static_telegram_header(b)
        return b

    def read_list(self, idn, offset, length):
        b = telegram_header_static('Listensegment lesen')
        b += payload_head(idn, Access.VALUE)

        b += bytearray(struct.pack('<h', offset))
        b += bytearray(struct.pack('<h', length))

        b = fill_length_into_static_telegram_header(b)
        b = fill_checksum_into_static_telegram_header(b)

        return b


