# Copyright (c) 2016, Nordic Semiconductor
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of Nordic Semiconductor ASA nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Setup script for nrfjprog.

USAGE:
    python setup.py install or python setup.py bdist_egg (to create a Python egg)
"""

#import fnmatch
import os
from setuptools import setup, find_packages
#import subprocess
import sys

from nrfjprog import nrfjprog_version


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_requirements(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).readlines()


setup(
    name='nRF5-universal-prog',
    version=nrfjprog_version.NRFJPROG_VERSION,
    description='The nRF5-universal-prog command line tool implemented in Python.',
    long_description=read('README.md'),
    url='https://github.com/NordicSemiconductor/nRF5-universal-prog',
    author='Nordic Semiconductor ASA',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Debuggers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='nRF5 nRF51 nRF52 nrfjprog pynrfjprog pyOCD Nordic Semiconductor SEGGER JLink',
    install_requires=read_requirements('requirements.txt'),
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=False
)

"""if __name__ == '__main__':
    print('#### Auto formatting all Python code in nRFTools according to PEP 8...')
    matches = []
    for root, dirnames, filenames in os.walk(
            os.path.dirname(os.path.realpath(__file__))):
        for filename in fnmatch.filter(filenames, '*.py'):
            matches.append(os.path.join(root, filename))
    for match in matches:
        subprocess.check_call(
            ["autopep8", "--in-place", "--aggressive", "--aggressive", match])"""
