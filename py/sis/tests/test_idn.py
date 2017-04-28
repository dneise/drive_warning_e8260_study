from sis import idn
from sis.idn import IDN


def test_IDN_ctor():
    i = IDN(idn.S, 0, 44)

    assert 44 == i.to_int()
    assert b',\x00' == bytes(i)
    assert str(i) == 'S-0-0044'


def test_from_string_works_at_all():
    name = 'S-0-0044'
    assert name == str(IDN.from_string(name))


def test_from_short_works_at_all():
    n = IDN(idn.S, 0, 44).to_int()
    assert n == IDN.from_short(n).to_int()


def test_from_bytes_works_at_all():
    b = bytes(IDN(idn.S, 0, 44))
    assert b == bytes(IDN.from_bytes(b))


def test_repr():
    i = IDN(idn.S, 0, 44)
    assert 'IDN(S-0-0044)' == repr(i)


def test_from_string_time():

    import timeit
    N = int(1e5)
    runtime = timeit.timeit(
        'IDN.from_string("P-0-0434")',
        setup='from sis.idn import IDN',
        number=N
    )
    assert runtime/N < 100e-6  # should be quicker than 100us on this platform.
