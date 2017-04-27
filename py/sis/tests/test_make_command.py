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

    from sis.make_command import read, S, P
    assert read_wichtungsart_speed() == read(S, 0, 44)


def test_type_set_number_from_string():

    from sis.make_command import type_set_number_from_string, S, P
    t, s, n = type_set_number_from_string('S-0-0044')
    assert t == S
    assert s == 0
    assert n == 44

    t, s, n = type_set_number_from_string('P-0-0434')
    assert t == P
    assert s == 0
    assert n == 434

    import timeit
    N = 1000000
    runtime = timeit.timeit(
        'type_set_number_from_string("P-0-0434")',
        setup='from sis.make_command import type_set_number_from_string',
        number=N
    )
    assert runtime/N < 10e-6  # should be quicker than 10us on this platform.
