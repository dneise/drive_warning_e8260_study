from sis.make_command import TelegramFactory, IDN


def test_parameter_request_with_known_working_example():

    def read_wichtungsart_speed():

        b = bytearray([
            0x02,   # STX constant 0x02
            0x00,   # checksum, to be filled later
            0x00,   # length, to be filled later
            0x00,   # length repetition
            0x00,   # ctrl: no sub addrs, no reaction, no packet number
            0x10,   # service: read:0x10, write: 0x1F
            100,    # sender address: 0..126
            128,    # receiver address: 128: point2point
            # dynamic part:
            #  no sub addresses
            #  no paket number
            0x3C,   # Betriebsdatum: 0x38; set bit 2: last transmission
            128,    # device address: just repeat the address above.
            0x00,   # Parameter Typ
            0x2C,   # -> S-0-0044
            0x00,   # /\
        ])

        L = len(b)
        b[2] = L - 8
        b[3] = L - 8
        b[1] = (-1 * sum(b)) & 0xFF  # checksum

        assert (sum(b) & 0xFF) == 0

        return b

    tf = TelegramFactory()
    assert read_wichtungsart_speed() == tf.read(IDN.from_string('S-0-0044'))

