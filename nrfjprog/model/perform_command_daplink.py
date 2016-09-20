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

import enum
from intelhex import IntelHex
import os
from pyOCD.board import MbedBoard
from pyOCD.target import cortex_m

from nrfjprog import nrfjprog_version
from nrfjprog.model import device
from nrfjprog.model.perform_command import PerformCommand


@enum.unique
class Memory_Access_Mode(enum.IntEnum):
    READ_ENABLE = 0
    WRITE_ENABLE = 1
    ERASE_ENABLE = 2


class DapLink(PerformCommand):
    """

    """

    def erase(self, args):
        board = self._setup()
        board.flash.init()

        NVMC_ERASEUICR_ADDR = 0x4001E514

        if args.erasepage:
            board.flash.erasePage(args.erasepage)
        elif args.eraseuicr:
            self._erase_uicr(board.target)
        else:
            board.flash.eraseAll()

    def halt(self, args):
        board = self._setup()
        board.target.halt()

    def ids(self, args):
        MbedBoard.listConnectedBoards()

    def memrd(self, args):
        board = self._setup()
        data = board.target.readBlockMemoryUnaligned8(args.addr, args.length)
        self.output_data(args.addr, data)

    def memwr(self, args):
        board = self._setup()

        # TODO: This should not be hard-coded.
        nRF5_device = device.NRF5xDevice('NRF52_FP1')

        if self.is_flash_addr(args.addr, nRF5_device):
            self._config_NVMC(board.target, Memory_Access_Mode.WRITE_ENABLE)
            board.target.write32(args.addr, args.val)
            self._config_NVMC(board.target, Memory_Access_Mode.READ_ENABLE)
        else:
            board.target.write32(args.addr, args.val)

    def pinresetenable(self, args):
        board = self._setup()
        assert(board.getTargetType() is 'nrf52')

        self._config_NVMC(board.target, Memory_Access_Mode.WRITE_ENABLE)

        uicr_pselreset0_addr = 0x10001200
        uicr_pselreset1_addr = 0x10001204
        # Writes the CONNECT and PIN bit fields (reset is connected and GPIO
        # pin 21 is selected as the reset pin).
        uicr_pselreset_21_connect = 0x15

        board.target.write32(uicr_pselreset0_addr, uicr_pselreset_21_connect)
        board.target.write32(uicr_pselreset1_addr, uicr_pselreset_21_connect)

        self._config_NVMC(board.target, Memory_Access_Mode.READ_ENABLE)

        board.target.reset()

    def program(self, args):
        board = self._setup()
        board.flash.init()

        tmp_bin_file = 'tmp.bin'

        if args.sectorsanduicrerase:
            # TODO: May not be needed if pyOCD does this. Double check before
            # removing.
            self._erase_uicr(board.target)

        hex_file = IntelHex(args.file)
        hex_file.tobinfile(tmp_bin_file)
        board.flash.flashBinary(
            tmp_bin_file,
            chip_erase=args.eraseall,
            fast_verify=args.verify)

        if args.debugreset or args.pinreset or args.systemreset:
            board.target.reset()

        os.remove(tmp_bin_file)

    def rbp(self, args):
        print('Not implemented in nrfjprog when using pyOCD.')

    def readregs(self, args):
        board = self._setup()

        for reg in cortex_m.CORE_REGISTER:
            if cortex_m.CORE_REGISTER[reg] in range(0, 16):
                print(board.target.readCoreRegister(reg))

    def readtofile(self, args):
        board = self._setup()
        # TODO: This should not be hard-coded.
        nRF5_device = device.NRF5xDevice('NRF52_FP1')

        try:
            with open(args.file, 'w') as file:
                if args.readcode or not (args.readuicr or args.readram):
                    file.write('----------Code FLASH----------\n\n')
                    self.output_data(
                        nRF5_device.flash_start,
                        board.target.readBlockMemoryAligned32(
                            nRF5_device.flash_start,
                            nRF5_device.flash_size),
                        file)
                    file.write('\n\n')
                if args.readuicr:
                    file.write('----------UICR----------\n\n')
                    self.output_data(
                        nRF5_device.uicr_start,
                        board.target.readBlockMemoryAligned32(
                            nRF5_device.uicr_start,
                            nRF5_device.page_size),
                        file)
                    file.write('\n\n')
                if args.readram:
                    file.write('----------RAM----------\n\n')
                    self.output_data(
                        nRF5_device.ram_start,
                        board.target.readBlockMemoryAligned32(
                            nRF5_device.ram_start,
                            nRF5_device.ram_size),
                        file)
        except IOError as error:
            pass  # TODO: do something...

    def recover(self, args):
        print('WARNING: This will not actually unlock the chip right now, just does a full erase.')
        board = self._setup()

        board.flash.init()
        board.flash.eraseAll()

    def reset(self, args):
        board = self._setup()
        board.target.reset()

    def run(self, args):
        board = self._setup()
        board.target.resume()

    def verify(self, args):
        board = self._setup()

        hex_file = IntelHex(args.file)
        for segment in hex_file.segments():
            start_addr, end_addr = segment
            size = end_addr - start_addr

            data = hex_file.tobinarray(start=start_addr, size=size)
            read_data = board.target.readBlockMemoryUnaligned8(
                start_addr, size)

            assert (self.byte_lists_equal(data, read_data)
                    ), 'Verify failed. Data readback from memory does not match data written.'

    def version(self, args):
        print('nRFjprog version: {}'.format(nrfjprog_version.NRFJPROG_VERSION))

    # Helpers.

    def _config_NVMC(self, target, access_mode):
        """
        Configure the NVMC to read, write, or erase FLASH.

        """
        NVMC_CONFIG_ADDR = 0x4001E504
        target.write32(NVMC_CONFIG_ADDR, access_mode)

    def _erase_uicr(self, target):
        self._config_NVMC(target, Memory_Access_Mode.ERASE_ENABLE)
        target.write32(NVMC_ERASEUICR_ADDR, 1)
        self._config_NVMC(target, Memory_Access_Mode.READ_ENABLE)

    def _setup(self):
        board = MbedBoard.chooseBoard()
        return board
