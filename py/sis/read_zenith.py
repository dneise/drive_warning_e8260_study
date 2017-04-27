import serial
import struct
import time
from pprint import pprint
from datetime import datetime, timedelta
import numpy as np
from tqdm import tqdm

S = 0
P = 1


def request_parameter(type_=S, set_=0, number=44):
    word = number
    word |= set_ << 12
    word |= type_ << 15
    lsb, msb = struct.pack("<H", word)

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
        0x00,   # Parameter Type if different from S or P (we don't use that).
        lsb,
        msb,
    ])

    L = len(b)
    b[2] = L - 8
    b[3] = L - 8
    b[1] = (-1 * sum(b)) & 0xFF  # checksum

    assert (sum(b) & 0xFF) == 0

    return b


def make_ser():
    ser = serial.Serial()
    ser.port = "COM10"
    ser.baudrate = 115200
    ser.timeout = 4
    ser.parity = serial.PARITY_NONE
    ser.open()

    assert ser.isOpen()
    return ser

d = {
    "Lage Istwert Geber 1": (S, 0, 51, 15, 1, '<i'),
    "Lage Sollwert": (S, 0, 47, 15, 1, '<i'),
    "Geschwindigkeits-Istwert": (S, 0, 40, 15, 1, '<i'),
    "Drehmoment Istwert": (S, 0, 84, 13, 1, '<h'),
    "Beschleunigungsistwert 1": (S, 0, 164, 15, 1e-6, '<i'),
}

a = np.zeros(len(d)+1, dtype=np.float64)


# Example
"""
Lage Istwert Geber 1 15 b'\x02\xe7\x07\x07\x10\x10\x80d\x00<\x80\x190\x00\x00'
Lage Istwert Geber 2 15 b'\x02\xe9\x07\x07\x10\x10\x80d\x00<\x80\x170\x00\x00'
Lage Sollwert 15 b'\x02\xe7\x07\x07\x10\x10\x80d\x00<\x80\x190\x00\x00'

Geschwindigkeits-Istwert 15 b'\x02v\x07\x07\x10\x10\x80d\x00<\x80\xbe\xfe\xff\xff'
Geschwindigkeits-Sollwert 15 b'\x020\x07\x07\x10\x10\x80d\x00<\x80\x00\x00\x00\x00'
Geschwindigkeits-Sollwert additiv 15 b'\x020\x07\x07\x10\x10\x80d\x00<\x80\x00\x00\x00\x00'

Drehmoment Sollwert 13 b'\x024\x05\x05\x10\x10\x80d\x00<\x80\x00\x00'
Drehmoment Sollwert additiv 13 b'\x024\x05\x05\x10\x10\x80d\x00<\x80\x00\x00'
Drehmoment Istwert 13 b'\x02;\x05\x05\x10\x10\x80d\x00<\x80\xfa\xff'

Motor Temperatur 13 b'\x02\xd4\x05\x05\x10\x10\x80d\x00<\x80`\x00'
Verstärker Temperatur 13 b'\x02\xb3\x05\x05\x10\x10\x80d\x00<\x80\x80\x01'

Beschleunigungsistwert 1 15 b'\x02O\x07\x07\x10\x10\x80d\x00<\x80 \xce\xf4\xff'
Beschleunigungsistwert 2 15 b'\x02\xd4\x07\x07\x10\x10\x80d\x00<\x80\x001\x08#'
"""


def req_n_receive_parameter(device, type_=S, set_=0, number=44, size_=13):
    b = request_parameter(type_, set_, number)
    device.write(b)
    device.flush()
    if size_ is not None:
        result = device.read(size_)
        if len(result) != size_:
            raise TimeoutError
    else:
        time.sleep(1)
        result = device.read(device.inWaiting())
    return result


def read_all(device, desc):
    results = {}
    global a
    for i, name in enumerate(sorted(desc)):
        r = req_n_receive_parameter(device, *desc[name][:-2])
        v = struct.unpack(desc[name][-1], r[8+3:])[0] * desc[name][-2]
        results[name] = v
        a[i+1] = v
    a[0] = time.time()
    return results

def read_all_dump_to_file(device, desc, file):
    global a
    for i, name in enumerate(sorted(desc)):
        r = req_n_receive_parameter(device, *desc[name][:-2])
        v = struct.unpack(desc[name][-1], r[8+3:])[0] * desc[name][-2]
        a[i+1] = v
    a[0] = time.time()
    a.tofile(file)


def make_path():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S_zenith.bin")

def readout_forever():
    ser = make_ser()
    req_n_receive_parameter(ser)  # just to see if the file is really open
    pbar = tqdm()
    path = make_path()
    print("opening: "+path)
    with open(path, "wb") as file:
        while True:
            r = read_all_dump_to_file(ser, d, file)
            pbar.update(1)


if __name__ == "__main__":
    for i, name in enumerate(sorted(d)):
        print(i, name)
    while True:
        try:
            readout_forever()
        except TimeoutError:
            time.sleep(10)
    

# --------------------------------------------------------------------------


def test_parameter_request_with_known_working_example():

    def request_wichtungsart_speed():

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

    assert request_wichtungsart_speed() == request_parameter(S, 0, 44)
