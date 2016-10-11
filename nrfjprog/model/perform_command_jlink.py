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

from pynrfjprog import API

from nrfjprog import nrfjprog_version
from nrfjprog.model import device
from nrfjprog.model.perform_command import PerformCommand


class SetupCommand(object):
    """Class that handles the pynrfjprog api instance, some shared arguments, and logging."""

    DEFAULT_JLINK_SPEED_KHZ = 5000

    def __init__(self, args, do_not_initialize_api=False):
        """
        Initialize the class's properties, sets up the connection to our target device, and configures some logging options.

        :param Object args:                  Arguments the command was called with.
        :param bool  do_not_initialize_api:  If api should be initialized (the connection to the target device should be set up - a command may not need to connect to the target device).
        """
        self.args = args
        self.api = None
        self.device = None
        self.device_version = None

        if not do_not_initialize_api:
            if self._setup('NRF52'):
                pass
            elif self._setup('NRF51'):
                pass
            else:
                assert(False), 'Unknown device family.'

    def cleanup(self):
        """
        Disconnect from the emulator (debugger) and close the pynrfjprog api instance.

        """
        self.api.disconnect_from_emu()
        self.api.close()
        self.api = None
        self.device = None
        self.device_version = None

    def connect_to_emu(self, api):
        """
        This method should only be called when this class is created with the do_not_initialize_api flag (i.e. called by recover()).

        :param API api: An instance of api that has been initialized by the caller.
        """
        assert (
            self.api is None), "The class's api property has already been initialized."
        self.api = api
        self._connect_to_emu()

    def _connect_to_emu(self):
        """
        Connect to the emulator (debugger) with the specific serial number and/or clock speed if either was specified in the command-line arguments.

        """
        if self.args.snr and self.args.clockspeed:
            self.api.connect_to_emu_with_snr(
                self.args.snr, self.args.clockspeed)
        elif self.args.snr:
            self.api.connect_to_emu_with_snr(
                self.args.snr, self.DEFAULT_JLINK_SPEED_KHZ)
        elif self.args.clockspeed:
            self.api.connect_to_emu_without_snr(self.args.clockspeed)
        else:
            self.api.connect_to_emu_without_snr(self.DEFAULT_JLINK_SPEED_KHZ)

    def _setup(self, device_family_guess):
        """
        Connect to target device and check if device_family_guess is correct. If correct, initialize api and device_version and return True. Else, cleanup and return False.

        :param  String device_family_guess: The device family type to try.
        :return Boolean: If device_family_guess was correct and we initialized everything successfully.
        """
        if self.args.jlink_arm_dll_path:
            self.api = API.API(device_family_guess,
                jlink_arm_dll_path=self.args.jlink_arm_dll_path)
        else:
            self.api = API.API(device_family_guess)
        self.api.open()
        self._connect_to_emu()

        if not self.args.deviceversion:
            try:
                self.device_version = self.api.read_device_version()
            except API.APIError as error:
                if error.err_code == API.NrfjprogdllErr.WRONG_FAMILY_FOR_DEVICE:
                    self.cleanup()
                    return False
                else:
                    assert(False), 'Error!'
        else:
            self.device_version = self.args.deviceversion

        self.device = device.NRF5xDevice(self.device_version)
        return True


class JLink(PerformCommand):
    """

    """

    def erase(self, args):
        nrf = SetupCommand(args)

        if args.erasepage:
            nrf.api.erase_page(args.erasepage)
        elif args.eraseuicr:
            nrf.api.erase_uicr()
        else:
            nrf.api.erase_all()

        nrf.cleanup()

    def halt(self, args):
        nrf = SetupCommand(args)

        nrf.api.halt()

        nrf.cleanup()

    def ids(self, args):
        nrf = SetupCommand(args, do_not_initialize_api=True)

        # Device family type arbitrary since we are not connecting to a device.
        # Use NRF52 by default.
        api = API.API('NRF52')
        api.open()

        ids = api.enum_emu_snr()
        if ids:
            print(sorted(ids))

        api.close()

    def memrd(self, args):
        nrf = SetupCommand(args)

        data = nrf.api.read(args.addr, args.length)
        self.output_data(args.addr, data)

        nrf.cleanup()

    def memwr(self, args):
        nrf = SetupCommand(args)

        nrf.api.write_u32(
            args.addr,
            args.val,
            self.is_flash_addr(
                args.addr,
                nrf.device))

        nrf.cleanup()

    def pinresetenable(self, args):
        nrf = SetupCommand(args)

        assert(
            nrf.device_version[
                :5] != 'NRF51'), "Enabling pin reset is not a valid command for nRF51 devices."

        uicr_pselreset0_addr = 0x10001200
        uicr_pselreset1_addr = 0x10001204
        # Writes the CONNECT and PIN bit fields (reset is connected and GPIO
        # pin 21 is selected as the reset pin).
        uicr_pselreset_21_connect = 0x15

        nrf.api.write_u32(
            uicr_pselreset0_addr,
            uicr_pselreset_21_connect,
            True)
        nrf.api.write_u32(
            uicr_pselreset1_addr,
            uicr_pselreset_21_connect,
            True)
        nrf.api.sys_reset()

        nrf.cleanup()

    def program(self, args):
        from intelhex import IntelHex
        nrf = SetupCommand(args)

        if args.eraseall:
            nrf.api.erase_all()
        if args.sectorsanduicrerase:
            nrf.api.erase_uicr()

        hex_file = IntelHex(args.file)
        for segment in hex_file.segments():
            start_addr, end_addr = segment
            size = end_addr - start_addr

            if args.sectorserase or args.sectorsanduicrerase:
                start_page = int(start_addr / nrf.device.page_size)
                end_page = int(end_addr / nrf.device.page_size)
                for page in range(start_page, end_page + 1):
                    nrf.api.erase_page(page * nrf.device.page_size)

            data = hex_file.tobinarray(start=start_addr, size=(size))
            nrf.api.write(start_addr, data.tolist(), True)

            if args.verify:
                read_data = nrf.api.read(start_addr, len(data))
                assert (
                    self.byte_lists_equal(
                        data, read_data)), 'Verify failed. Data readback from memory does not match data written.'

        self._reset(nrf, args)

        nrf.cleanup()

    def rbp(self, args):
        nrf = SetupCommand(args)

        if args.rbplevel == 'CR0':
            nrf.api.readback_protect(API.ReadbackProtection.REGION_0)
        else:
            nrf.api.readback_protect(API.ReadbackProtection.ALL)

        nrf.cleanup()

    def readregs(self, args):
        nrf = SetupCommand(args)

        for reg in API.CpuRegister:
            print(
                '{}: {}'.format(
                    reg.name, hex(
                        nrf.api.read_cpu_register(reg))))

        nrf.cleanup()

    def readtofile(self, args):
        nrf = SetupCommand(args)

        try:
            with open(args.file, 'w') as file:
                if args.readcode or not (args.readuicr or args.readram):
                    file.write('----------Code FLASH----------\n\n')
                    self.output_data(
                        nrf.device.flash_start,
                        nrf.api.read(
                            nrf.device.flash_start,
                            nrf.device.flash_size),
                        file)
                    file.write('\n\n')
                if args.readuicr:
                    file.write('----------UICR----------\n\n')
                    self.output_data(
                        nrf.device.uicr_start,
                        nrf.api.read(
                            nrf.device.uicr_start,
                            nrf.device.page_size),
                        file)
                    file.write('\n\n')
                if args.readram:
                    file.write('----------RAM----------\n\n')
                    self.output_data(
                        nrf.device.ram_start, nrf.api.read(
                            nrf.device.ram_start, nrf.device.ram_size), file)
        except IOError as error:
            print("{}.".format(error))

        nrf.cleanup()

    def recover(self, args):
        nrf = SetupCommand(args, do_not_initialize_api=True)

        api = API.API(args.family)
        api.open()

        nrf.connect_to_emu(api)
        nrf.api.recover()

        nrf.cleanup()

    def reset(self, args):
        nrf = SetupCommand(args)

        self._reset(nrf, args, default_sys_reset=True)

        nrf.cleanup()

    def run(self, args):
        nrf = SetupCommand(args)

        if args.pc is not None and args.sp is not None:
            nrf.api.run(args.pc, args.sp)
        elif args.pc is not None or args.sp is not None:
            assert(False), 'Both the PC and the SP must be specified.'
        else:
            nrf.api.go()

        nrf.cleanup()

    def verify(self, args):
        from intelhex import IntelHex
        nrf = SetupCommand(args)

        hex_file = IntelHex(args.file)
        for segment in hex_file.segments():
            start_addr, end_addr = segment
            size = end_addr - start_addr

            data = hex_file.tobinarray(start=start_addr, size=size)
            read_data = nrf.api.read(start_addr, size)

            assert (self.byte_lists_equal(data, read_data)
                    ), 'Verify failed. Data readback from memory does not match data written.'

        nrf.cleanup()

    def version(self, args):
        nrf = SetupCommand(args, do_not_initialize_api=True)

        api = API.API('NRF52')
        api.open()

        jlink_arm_dll_version = api.dll_version()
        print('JLink version: {}'.format(jlink_arm_dll_version))
        print('nRFjprog version: {}'.format(nrfjprog_version.NRFJPROG_VERSION))

        api.close()

    # Helper functions.

    def _reset(self, nrf, args, default_sys_reset=False):
        """
        Reset and run the device.

        """
        if args.debugreset:
            nrf.api.debug_reset()
        elif args.pinreset:
            nrf.api.pin_reset()
        elif args.systemreset or default_sys_reset:
            nrf.api.sys_reset()
        else:
            return

        nrf.api.go()
