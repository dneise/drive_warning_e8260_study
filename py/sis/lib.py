import serial
import struct
import time
from pprint import pprint
from datetime import datetime, timedelta
import numpy as np
from tqdm import tqdm
import make_command as cmd


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

