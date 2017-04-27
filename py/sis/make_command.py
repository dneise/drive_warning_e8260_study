import struct

S = 0
P = 1
STX = 0x02
type_map = {
    'S': S,
    'P': P,
}


status_byte_meaning = {
    0x00: 'fehlerfreie Übertragung - ohne Fehler',
    0x01: 'Bei der Ausführung des angeforderten Dienstes Ausführungsfehler ist ein Fehler aufgetreten. Der dienstspezifische Fehlercode steht in den Nutzdaten des Reaktionstelegramms.',
    0xF0: 'Der angeforderte Dienst wird vom adressierten Slave nicht unterstützt. Telegrammfehler',
    0xF8: 'Im Folgetelegramm haben sich Daten im Nutzdatenkopf, die Senderadresse oder der Dienstgeändert. Telegrammfehler',
    0xF9: 'Das Befehlstelegramm enthält Sub-Adressen. Das Durchreichen von Telegrammen wird vom Slave nicht unterstützt.Telegrammfehler',
    0xFA: 'Im Befehlstelegramm fehlen Nutzdaten. Das Telegramm kann nicht ausgeführt werden. Telegrammfehler',
    0xFB: 'Der angeforderte Subdienst wird im adressierten Slave nicht unterstützt. Telegrammfehler',
    0xFC: 'Die angeforderte Komponente ist im adressierten Slave nicht vorhanden. Die Komponentenadresse ist ungültig. Telegrammfehler',
}

fehlercode_dienst_beschreibung = {
    (0x0700, 0x03): 'nicht unterstützte Baudrate',
    (0x0800, 0x03): 'nicht unterstützte Baudrate',
    (0x800C, 0x80): 'Zugriff auf Parameter verweigert; der Parameter ist vom Folgetelegrammkanal belegt.',
    (0x800C, 0x81): 'Zugriff auf Parameter verweigert; der Parameter ist vom Folgetelegrammkanal belegt.',
    (0x800C, 0x8E): 'Zugriff auf Parameter verweigert; der Parameter ist vom Folgetelegrammkanal belegt.',
    (0x800C, 0x8F): 'Zugriff auf Parameter verweigert; der Parameter ist vom Folgetelegrammkanal belegt.',
    (0x9002, 0x02): 'Firmware wurde gelöscht',
    (0x9004, 0x02): 'Shutdown in Phase 4 nicht erlaubt (in FWA-MTx01VRSanstelle von 0x9010)',
    (0x9010, 0x02): 'Shutdown im Betriebsmodus nicht erlaubt (ab FWA-MPx02VRS)',
    (0x9102, 0x02): 'Firmware wurde gelöscht',
    (0x9104, 0x02): 'Reboot in Phase 4 nicht erlaubt (in FWA-MTx01VRS anstelle von 0x9110)',
    (0x9110, 0x02): 'Reboot im Betriebsmodus nicht erlaubt (ab FWA-MPx02VRS)',
    (0x9200, 0x02): 'Fehler beim Lesen',
    (0x920B, 0x02): 'Die angeforderte Datenmenge überschreitet die max.Nutzdatenmenge im Reaktionstelegramm.',
    (0x9400, 0x02): 'Timeout während Löschvorgang',
    (0x940A, 0x02): 'Löschen nur in Loader möglich',
    (0x96E0, 0x02): 'Verify-Fehler beim Programmieren des Flashs',
    (0x96E1, 0x02): 'Timeout beim Programmieren des Flashs',
    (0x96FF, 0x02): 'Fehler beim Schreiben ins Flash',
    (0x9701, 0x02): 'Additions-Checksumme fehlerhaft',
    (0x9702, 0x02): 'CRC32-Checksumme fehlerhaft',
    (0xA001, 0x02): 'Fehler beim Einlesen der Tabelle',
    (0xA002, 0x02): 'falscher Tabellentyp',
    (0xA003, 0x02): 'kein Backup-Medium vorhanden',
    (0xA201, 0x02): 'Fehler beim Einlesen des Hex-Headers',
    (0xA202, 0x02): 'falsche Headernummer',
    (0xA501, 0x02): 'Fehler beim Schreiben',
    (0xA502, 0x02): 'Anlegen der Datei nicht erlaubt',
    (0xA503, 0x02): 'nicht genügend Speicherplatz',
    (0xA601, 0x02): 'Fehler beim Schreiben',
    (0xA602, 0x02): 'Zugriff auf die Datei nicht erlaubt',
}

dienste_und_subdienste = {
    (0x00, 0x01): 'SIS-Version lesen',
    (0x00, 0x02): 'Firmware-Version lesen',
    (0x00, 0x03): 'Typ des Regelgerätes lesen',
    (0x00, 0x04): 'unterstützte Baudraten lesen',

    (0x01, None): 'Abbruch der Datenübertragung',

    (0x02, 0x90): 'Shutdown',
    (0x02, 0x91): 'Reboot',
    (0x02, 0x92): 'Read Flash',
    (0x02, 0x93): 'Find Header',
    (0x02, 0x94): 'Erase Flash',
    (0x02, 0x96): 'Program Flash',
    (0x02, 0x97): 'Build Checksum',
    (0x02, 0x9F): 'Fehler-Reset im Slave',
    (0x02, 0xA0): 'Read Configuration',
    (0x02, 0xA2): 'Read Header',
    (0x02, 0xA5): 'Write File Info',
    (0x02, 0xA6): 'Write File Data',

    (0x03, 0x01): 'Festlegung TrS',
    (0x03, 0x02): 'Festlegung TzA',
    (0x03, 0x03): 'Festlegung Tmas',
    (0x03, 0x07): 'Festlegung der Baudrate',
    (0x03, 0x08): 'zeitgesteuerter Baudratentest',
    (0x03, 0xFF): 'Übernahme der festgelegten Werte',

    (0x10, None): 'Parameter lesen',
    (0x11, None): 'Listensegment lesen',
    (0x1E, None): 'Listensegment schreiben',
    (0x1F, None): 'Parameter schreiben',

    (0x80, None): 'Parameter lesen',
    (0x81, None): 'Listensegment lesen',
    (0x8E, None): 'Listensegment schreiben',
    (0x8F, None): 'Parameter schreiben',
}

fehlercodes = {
    4097: 'IDN nicht vorhanden',
    4105: 'falscher Zugriff auf Element 1',
    8193: 'Name nicht vorhanden',
    8194: 'Name zu kurz übertragen',
    8195: 'Name zu lang übertragen',
    8196: 'Name nicht änderbar',
    8197: 'Name zur Zeit schreibgeschützt',
    12290: 'Attribut zu kurz übertragen',
    12291: 'Attribut zu lang übertragen',
    12292: 'Attribut nicht änderbar',
    12293: 'Attribut zur Zeit schreibgeschützt',
    16385: 'Einheit nicht vorhanden',
    16386: 'Einheit zu kurz übertragen',
    16387: 'Einheit zu lang übertragen',
    16388: 'Einheit nicht änderbar',
    16389: 'Einheit zur Zeit schreibgeschützt',
    20481: 'minimaler Eingabewert nicht vorhanden',
    20482: 'minimaler Eingabewert zu kurz übertragen',
    20483: 'minimaler Eingabewert zu lang übertragen',
    20484: 'minimaler Eingabewert nicht änderbar',
    20485: 'minimaler Eingabewert zur Zeit schreibgeschützt',
    24577: 'maximaler Eingabewert nicht vorhanden',
    24578: 'Maximaler Eingabewert zu kurz übertragen',
    24579: 'maximaler Eingabewert zu lang übertragen',
    24580: 'maximaler Eingabewert nicht änderbar',
    24581: 'maximaler Eingabewert zur Zeit schreibgeschützt',
    28674: 'Datum zu kurz übertragen',
    28675: 'Datum zu lang übertragen',
    28676: 'Datum nicht änderbar',
}

element_access_code = {
    'channel not active': 0b000,
    'ident-number': 0b001,
    'name': 0b010,
    'attribute': 0b011,
    'unit': 0b100,
    'min_value': 0b101,
    'max_value': 0b110,
    'value': 0b111,
}

simple_services = {
    name: dienst
    for (dienst, subdienst), name in dienste_und_subdienste.items()
    if subdienst is None and dienst < 0x80
}


def type_set_number_from_string(s):
    '''
    s like 'S-0-0044' or 'P-0-0434'
    '''
    type_ = type_map[s[0]]
    set_ = int(s[2])
    assert set_ in [0, 1]
    number = int(s[4:])
    return type_, set_, number


def telegram_header_static(
    sender_address=100,
    receiver_address=128,
    service_name='Parameter lesen'
        ):
    return bytearray([
        STX,
        0x00,   # checksum, to be filled later
        0x00,   # length, to be filled later
        0x00,   # length repetition
        make_telegram_head_ctrl_byte(
            number_of_dynamic_subadresses=0,
            has_paket_number=False,
            is_reaction_telegram=False,
        ),
        simple_services[service_name],
        sender_address,    # sender address: 0..126
        receiver_address,    # receiver address: 128: point2point
    ])


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


def payload_head(type_, set_, number, receiver_address, eac):
    word = number
    word |= set_ << 12
    word |= type_ << 15
    lsb, msb = struct.pack("<H", word)

    return bytearray([
        payload_ctrl_byte(eac),
        receiver_address,
        0x00,  # should be static like this
        lsb,
        msb,
    ])


def payload_ctrl_byte(eac):
    v = element_access_code[eac] << 3
    v |= 1 << 2
    return v


def read(type_, set_, number):
    sender_address = 100
    receiver_address = 128

    b = bytearray()
    b += telegram_header_static(
        sender_address=sender_address,
        receiver_address=receiver_address,
        service_name='Parameter lesen',
    )

    b += payload_head(
        type_=type_,
        set_=set_,
        number=number,
        receiver_address=receiver_address,
        eac='value',
    )

    b = fill_length_into_static_telegram_header(b)
    b = fill_checksum_into_static_telegram_header(b)

    return b


def write(type_, set_, number, value, size=2):
    sender_address = 100
    receiver_address = 128

    b = bytearray()
    b += telegram_header_static(
        sender_address=sender_address,
        receiver_address=receiver_address,
        service_name='Parameter schreiben',
    )

    b += payload_head(
        type_=type_,
        set_=set_,
        number=number,
        receiver_address=receiver_address,
        eac='value',
    )

    if size == 2:
        b += bytearray(struct.pack('<h', value))
    elif size == 4:
        b += bytearray(struct.pack('<i', value))

    b = fill_length_into_static_telegram_header(b)
    b = fill_checksum_into_static_telegram_header(b)

    return b


def check_response(r):
    # example b'\x022\x05\x05\x10\x10\x80d\x00<\x80\x02\x00'
    assert sum(r) % 256 == 0
    assert r[0] == STX
    assert len(r) - 8 == r[2]
    assert len(r) - 8 == r[3]
    assert r[4] == make_telegram_head_ctrl_byte(
        number_of_dynamic_subadresses=0,
        has_paket_number=False,
        is_reaction_telegram=True)
    assert r[5] in simple_services.values()
    assert r[6] == 128  # receiver address
    assert r[7] == 100  # master address
    assert r[8] in status_byte_meaning
    assert r[10] == 128


def get_status(r):
    return status_byte_meaning[r[8]]


def get_service(r):
    return dienste_und_subdienste[(r[5], None)]
