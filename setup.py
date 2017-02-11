import os
from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        f.read()

name = 'homepdu'

setup(
    name = name,
    version = '0.0.1',
    author = 'Filip Żyźniewski',
    author_email = 'filip.zyzniewski@gmail.com',
    description = 'Controlling home appliances using a power distribution unit',
    license = 'GPLv3',
    keywords = 'pdu snmp dpms',
    url = 'http://packages.python.org/homepdu',
    packages=[name],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Home Automation',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
