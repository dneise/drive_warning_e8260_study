import struct
from .make_command import make_telegram_head_ctrl_byte
from .make_command import TelegramFactory
from .lookup import dienste_und_subdienste, status_byte_meaning

class Response:

    def __init__(self, r, assert_checksum_and_length=True, wordsize=2):
        ''' r=b'\x022\x05\x05\x10\x10\x80d\x00<\x80\x02\x00'
        '''
        self.r = r
        self.wordsize = wordsize
        if assert_checksum_and_length:
            assert sum(self.r) % 256 == 0
            assert r[0] == TelegramFactory.STX
            assert len(r) - 8 == r[2]
            assert len(r) - 8 == r[3]

        '''
        assert r[4] == make_telegram_head_ctrl_byte(
            number_of_dynamic_subadresses=0,
            has_paket_number=False,
            is_reaction_telegram=True)
        '''
    def __repr__(self):

        s = "{cn}(value={v}".format(
                cn=self.__class__.__name__,
                v=self.value,
            )
        if not self.checksum_ok:
            s += ",\n checksum=False"

        if not self.r[8] == 0:
            s += ",\n status=" + self.status_string

        s += ")"
        return s

    @property
    def status_string(self):
        return status_byte_meaning.get(self.r[8], self.r[8])

    @property
    def service_string(self):
        return dienste_und_subdienste.get((self.r[5], None), self.r[5])

    @property
    def checksum_ok(self):
        return sum(self.r) % 256 == 0

    @property
    def value(self):
        L = len(self.r) - 11
        buf = self.r[11:]

        if self.wordsize == 2:
            return [x[0] for x in struct.iter_unpack('<h', buf)]
        elif self.wordsize == 4:
            return [x[0] for x in struct.iter_unpack('<i', buf)]
        else:
            return buf
