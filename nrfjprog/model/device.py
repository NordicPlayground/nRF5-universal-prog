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
Device specific info.

"""

FLASH_SIZE = {'NRF52_FP1': 0x80000,
              'NRF52_FP1_ENGB': 0x80000,
              'NRF52_FP1_ENGA': 0x80000,
              'NRF51_XLR3LC': 0x40000,
              'NRF51_XLR3P': 0x40000,
              'NRF51_L3': 0x20000,
              'NRF51_XLR3': 0x40000,
              'NRF51_XLR2': 0x40000,
              'NRF51_XLR1': 0x40000}

RAM_SIZE = {'NRF52_FP1': 0x10000,
            'NRF52_FP1_ENGB': 0x8000,
            'NRF52_FP1_ENGA': 0x4000,
            'NRF51_XLR3LC': 0x4000,
            'NRF51_XLR3P': 0x8000,
            'NRF51_L3': 0x4000,
            'NRF51_XLR3': 0x4000,
            'NRF51_XLR2': 0x4000,
            'NRF51_XLR1': 0x4000}

PAGE_SIZE = {'NRF52_FP1': 0x1000,
             'NRF52_FP1_ENGB': 0x1000,
             'NRF52_FP1_ENGA': 0x1000,
             'NRF51_XLR3LC': 0x400,
             'NRF51_XLR3P': 0x400,
             'NRF51_L3': 0x400,
             'NRF51_XLR3': 0x400,
             'NRF51_XLR2': 0x400,
             'NRF51_XLR1': 0x400}


class NRF5xDevice(object):
    """
    Class representing an nRF5x device.

    """

    flash_start = 0x0
    ram_start = 0x20000000
    ficr_start = 0x10000000
    uicr_start = 0x10001000

    def __init__(self, device_version):
        """
        Initialize the device specific specs.

        """
        self.flash_size = FLASH_SIZE[device_version]
        self.ram_size = RAM_SIZE[device_version]
        self.page_size = PAGE_SIZE[device_version]

        self.flash_end = self.flash_start + self.flash_size
        self.ram_end = self.ram_start + self.ram_size
        self.ficr_end = self.ficr_start + self.page_size
        self.uicr_end = self.uicr_start + self.page_size

        self.number_of_flash_pages_in_code = self.flash_size / self.page_size
