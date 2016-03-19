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

from pynrfjprog import API, Hex
import nrfjprog_version
import os

def _setup():
    """
    Discovers the family of the target device and connects to it.

    :return API: Instance of an API object that is connected to an nRF5x device.
    """
    device_family = API.DeviceFamily.NRF51
    api = API.API(device_family)
    api.open()
    api.connect_to_emu_without_snr()
    
    try:
        device_version = api.read_device_version()
    except API.APIError as e:
        if e.err_code == API.NrfjprogdllErr.WRONG_FAMILY_FOR_DEVICE:
            device_family = API.DeviceFamily.NRF52
            api.close()
            api = API.API(device_family)
            api.open()
            api.connect_to_emu_without_snr()
        else:
            raise e

    api.connect_to_device()

    assert(api.is_connected_to_device()), 'unable to connect to target device'
    return api

def _cleanup(api):
    api.close()

def erase(args):
    print('erasing device')
    api = _setup()

    if args.erasepage:
        api.erase_page(args.erasepage) # TODO: Not working.
    elif args.eraseuicr:
        api.erase_uicr()
    else:
        api.erase_all()

    _cleanup(api)

def ids(args):
    print('displaying ids of all connected debuggers')
    api = _setup()
    print(api.enum_emu_snr())
    _cleanup(api)

def program(args):
    print('programming device')
    api = _setup()

    module_dir, module_file = os.path.split(__file__)
    hex_file_path = os.path.join(os.path.abspath(module_dir), args.file.name)
    
    # Parse hex, program to device
    print('# Parsing hex file into segments  ')
    test_program = Hex.Hex(hex_file_path) # Parse .hex file into segments
    print('# Writing %s to device  ' % hex_file_path)
    for segment in test_program:
        api.write(segment.address, segment.data, True)

    _cleanup(api)

def recover(args):
    print('recovering device')
    api = _setup()

    api.recover()

    _cleanup(api)

def reset(args):
    """
    Performs a reset of the device. Performs a system reset by default.

    :param : The optional flags specified.
    """
    print('resetting device')
    api = _setup()

    if args.debugreset:
        api.debug_reset()
    elif args.pinreset:
        api.pin_reset()
    else:
        api.sys_reset()
    
    api.go()
    _cleanup(api)

def verify(args):
    """
    Verifies that memory contains the right data.

    """
    print('verifying memory of device')

def version(args):
    """
    Display the nrfjprog and JLinkARM DLL versions.

    """
    print('displaying the nrfjprog and JLinkARM DLL versions.')
    api = _setup()
    jlink_arm_dll_version = api.dll_version()
    print(jlink_arm_dll_version)
    print(nrfjprog_version.NRFJPROG_VERSION)
    _cleanup(api)