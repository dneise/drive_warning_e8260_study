import struct


class IDN:
    SP2int = {'S': 0, 'P': 1}
    int2SP = {v: k for k, v in SP2int.items()}

    def __init__(self, type_, set_, number):
        self.type_ = type_
        self.set_ = set_
        self.number = number

    @classmethod
    def from_string(cls, s):
        '''
        s like 'S-0-0044' or 'P-0-0434'
        '''
        type_ = IDN.SP2int[s[0]]
        set_ = int(s[2])
        assert set_ in [0, 1]
        number = int(s[4:])
        return cls(type_, set_, number)

    @classmethod
    def from_short(cls, n):
        type_ = n >> 15
        set_ = (n & 0x7000) >> 12
        number = n & 0x0FFF
        return cls(type_, set_, number)

    @classmethod
    def from_bytes(cls, b):
        ''' assume 2 bytes in little endian order
        '''
        return IDN.from_short(struct.unpack('<H', b)[0])

    def __str__(self):
        return "{t}-{s}-{n:04d}".format(
            t=IDN.int2SP[self.type_],
            s=self.set_,
            n=self.number)

    def __repr__(self):
        return "{s.__class__.__name__}({s!s})".format(s=self)

    def __bytes__(self):
        return struct.pack('<H', self.to_int())

    def to_int(self):
        i = self.number
        i |= self.set_ << 12
        i |= self.type_ << 15
        return i
