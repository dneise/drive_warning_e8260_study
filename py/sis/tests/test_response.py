from sis.response import Response


def test_ctor():
    r = Response(r=b'\x022\x05\x05\x10\x10\x80d\x00<\x80\x02\x00')

    assert 'Parameter lesen' == r.service_string
    assert 'fehlerfreie Übertragung - ohne Fehler' == r.status_string
    assert True == r.checksum_ok
    assert [(2,)] == r.value
