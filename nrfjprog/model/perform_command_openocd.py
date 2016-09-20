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

import subprocess

from nrfjprog import nrfjprog_version
from nrfjprog.model import device
from nrfjprog.model.perform_command import PerformCommand


class OpenOCD(PerformCommand):
    """
    Note: Missing some functions and program not working all the time.

    Probably will need --family arugment to determine which target/nrf5x.cfg script to use - until this is shared in openOCD.
    """

    def _create_shell_command(self, command):
        return [
            'sudo',
            'openocd',
            '-f',
            'interface/cmsis-dap.cfg',
            '-f',
            'target/nrf52.cfg',
            '-c',
            'init',
            '-c',
            command,
            '-c',
            'exit']

    def erase(self, args):
        command = 'nrf52 mass_erase'
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def halt(self, args):
        command = 'halt'
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def ids(self, args):
        command = 'targets'
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def memrd(self, args):
        command = 'mdw ' + str(args.addr) + ' ' + str(args.length)
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def memwr(self, args):
        """
        Not working.

        """
        command = 'mww ' + str(args.addr) + ' ' + str(args.val) + ' ' + str(1)
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def program(self, args):
        command = 'program ' + args.file + ' verify reset'
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def readregs(self, args):
        command = 'reg'
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def reset(self, args):
        command = 'reset'
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def run(self, args):
        command = 'resume ' + str(args.pc)
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)

    def version(self, args):
        print('nRFjprog version: {}'.format(nrfjprog_version.NRFJPROG_VERSION))
        command = 'version'
        shell_command = self._create_shell_command(command)
        subprocess.check_call(
            shell_command,
            stdin=None,
            stdout=None,
            stderr=None,
            shell=False)
