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
This module receives user input from __main__.py and performs the operation via JLink (pynrfjprog), DAP-Link/CMSIS-DAP (pyOCD) or openOCD.

"""


class PerformCommand(object):
    """Base class."""

    def byte_lists_equal(self, data, read_data):
        """Return True if two lists of bytes are identical"""
        for i in xrange(len(data)):
            if data[i] != read_data[i]:
                return False
        return True

    def is_flash_addr(self, addr, device):
        """Return True if addr is in a FLASH region, False if not."""
        return addr in range(
            device.flash_start,
            device.flash_end) or addr in range(
            device.uicr_start,
            device.uicr_end)

    def log(self, args, msg):
        """Print log to stdout unless user has specified --quiet."""
        if args.quiet:
            pass
        else:
            print(msg)

    def output_data(self, addr, byte_array, file=None):
        """Read data from memory and output it to the console or file with the following format: ADDRESS: WORD\n"""
        index = 0

        while index < len(byte_array):
            string = "{}: {}".format(hex(addr), byte_array[index: index + 4])
            if file:
                file.write(string + '\n')
            else:
                print(string)
            addr = addr + 4
            index = index + 4
