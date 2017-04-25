# coding: utf-8
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from astropy.table import Table
import pandas as pd
import numpy as np

def read_txt(path, sampling_period_in_ms=None):
    if sampling_period_in_ms is None:
        raise ValueError('sampling_period_in_ms has to be a number')
    df = pd.read_csv(
        path,
        delimiter=';',
        decimal=b',',
        index_col=False
    )
    df.index *= sampling_period_in_ms
    return df


def parse_tree(path):
    return ET.fromstring(open(path, encoding='ISO-8859-1').read())


def measurement(et):
    d = {}
    for signal in et[0][1][1][-1]:
        try:
            name = signal.attrib['Name']
            text = signal.attrib['Text']
            nice_name = text.split(name)[-1]
            nice_name += "({0})".format(signal.attrib['YUnit'])
            index = [float(p.attrib['X']) for p in signal if 'X' in p.attrib]
            d[nice_name] = [float(p.attrib['Y']) for p in signal if 'Y' in p.attrib]
        except:
            pass
    return pd.DataFrame(data=d, index=index)


def read(path, sampling_period_in_ms=None):
    if path.endswith('txt'):
        return read_txt(path, sampling_period_in_ms)
    else:
        return measurement(parse_tree(path))


def data(path, sampling_period_in_ms=None):
    df = read(path, sampling_period_in_ms)

    end_time = datetime.strptime(path.split('__')[0], "%Y%m%d/%H%M")
    td = pd.to_timedelta(df.index, unit='ms')
    df['time'] = end_time
    df['time'] -= td.max()
    df['time'] += td
    df.set_index('time', inplace=True)
    return df


def make_multipage_pdf():
    from glob import glob
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt

    with PdfPages('multipage_pdf.pdf') as pdf:
        dfs = []
        paths = sorted(glob('*/*.xmlz'))
        paths = [x for x in paths if 'test' not in x]
        for path in paths:
            print(path)

            fig, axes = plt.subplots(4, sharex=True, figsize=(8, 14))
            df = data(path)
            dfs.append(df)
            for i, name in enumerate(df.columns):
                axes[i].plot(df[name], '.')
                axes[i].set_ylabel(name)
            axes[-1].set_xlabel('time')
            plt.suptitle(path)
            pdf.savefig()
            plt.close()

        dd = pd.concat(dfs)
        fig, axes = plt.subplots(4, sharex=True, figsize=(8, 14))
        i = 0
        for name in dd.columns:
            if 'stwert' in name:
                axes[i].plot(dd[name], '.')
                axes[i].set_ylabel(name)
                i += 1
        pdf.savefig()
        plt.close()


def read_and_prepare_rexroth_file(path, sampling_period_in_ms=None):
    df = read(path, sampling_period_in_ms)
    df['sample_time'] = df.index.values - df.index.values[0]
    for name in df.columns:
        if 'Lage-Istwert' in name:
            df['pos'] = df[name]

    # this seems to be the difference between this and the aux files Az value
    df.pos -= 1.3333

    return df


def read_and_prepare_pointing_position_file(path):
    aux = Table.read(path)
    aux = aux.to_pandas()
    aux['Time'] = pd.to_datetime(aux.Time, unit='d')
    aux.set_index('Time', inplace=True)

    return aux


def assign_realtime(df, aux):
    a = df.pos.values[::100]
    az = aux.Az.resample('1s').bfill()

    r = []
    N = a.shape[0]
    for i in range(az.shape[0] - N - 1):
        r.append(((az.values[i:i+N] - a)**2).sum())
    r = np.array(r)

    start_time = az.index[r.argmin()] + pd.to_timedelta(1, unit='s')
    df['Time'] = start_time + pd.to_timedelta(df.sample_time, unit='ms')
    df.reset_index(inplace=True)
    df.set_index('Time', inplace=True)
    df.drop(['index', 'sample_time'], axis=1, inplace=True)
    return df


def main():
    df = read_and_prepare_xml_file('DriveTest20170420/Trigger90PercentTorque.xml')
    aux = read_and_prepare_pointing_position_file('aux/20170420.DRIVE_CONTROL_POINTING_POSITION.fits')
    df = assign_realtime(df, aux)
    return df

if __name__ == "__main__":
    make_multipage_pdf()
