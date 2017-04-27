
from setuptools import setup
from sis import __version__


setup(
    name='sis',
    version=__version__,
    description='sis',
    url='https://github.com/dneise/drive_warning_e8260_study/tree/master/py',
    author='Dominik Neise',
    author_email='neised@phys.ethz.ch',
    license='MIT',
    packages=[
        'sis',
    ],
    package_data={
    },
    tests_require=['pytest>=3.0.0'],
    setup_requires=['pytest-runner'],
    install_requires=[
        'numpy',
        'pyserial',
        'tqdm',
    ],
    zip_safe=False,
)
