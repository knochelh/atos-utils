#
# Copyright (C) STMicroelectronics Ltd. 2012
#
# This file is part of ATOS.
#
# ATOS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v2.0
# as published by the Free Software Foundation
#
# ATOS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# v2.0 along with ATOS. If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import re
import shlex
import logging
import subprocess
import select
import fcntl
import signal
import cStringIO

def cmdline2list(cmd):
    """
    Returns a list of args from the given shell command string.
    """
    return shlex.split(cmd)

def list2cmdline(args):
    """
    Returns a quoted string suitable for execution from a shell.
    Ref to http://stackoverflow.com/questions/967443/
      python-module-to-shellquote-unshellquote.
    """
    _quote_pos = re.compile('(?=[^-0-9a-zA-Z_./\n])')

    def quote(arg):
        r"""
        >>> quote('\t')
        '\\\t'
        >>> quote('foo bar')
        'foo\\ bar'
        """
        # This is the logic emacs uses
        if arg:
            return _quote_pos.sub('\\\\', arg).replace('\n', "'\n'")
        else:
            return "''"
    return ' '.join([quote(a) for a in args])

def _process_output(process, output_file, print_output, output_stderr):
    """
    Handles outputs in stdout/stderr until process end.
    """
    def setfl(fil, flg=None, msk=None):
        # set given flags/mask and return initial flag list
        flags = flg or fcntl.fcntl(fil, fcntl.F_GETFL)
        new_flags = msk and (flags | msk) or flags
        if not fil.closed:
            fcntl.fcntl(fil, fcntl.F_SETFL, new_flags)
        return flags
    # set flags to get non-blocking read of stdio/stderr
    errflags = setfl(process.stderr, msk=os.O_NONBLOCK)
    outflags = setfl(process.stdout, msk=os.O_NONBLOCK)
    try:
        while True:
            # wait for new data avalaible or process end
            ready = select.select(
                [process.stderr, process.stdout], [], [])[0]
            if process.stderr in ready:
                data = process.stderr.read()
                if data and output_stderr: output_file.write(data)
                if data and print_output: sys.stderr.write(data)
            if process.stdout in ready:
                data = process.stdout.read()
                if data: output_file.write(data)
                if data and print_output: sys.stdout.write(data)
            if process.poll() is not None:
                break
    finally:
        # reset initial flags
        setfl(process.stdout, flg=outflags)
        setfl(process.stderr, flg=errflags)

def _subcall(cmd, get_output=False, print_output=False, output_stderr=False):
    """
    Executes given command.
    Returns exit_code and output.

    Returned output will be None unless get_output argument is set.
    Stderr will be included in returned output if output_stderr is set.
    Outputs will not be printed on stdout/stderr unless print_output is set.
    """
    if isinstance(cmd, str):
        cmd = cmdline2list(cmd)
    outputf = get_output and cStringIO.StringIO()
    popen_kwargs = {}
    if get_output or not print_output:
        popen_kwargs = {'stdout': subprocess.PIPE, 'stderr': subprocess.PIPE}
    process = subprocess.Popen(cmd, **popen_kwargs)
    while True:
        try:
            if get_output:
                _process_output(
                    process, output_file=outputf, print_output=print_output,
                    output_stderr=output_stderr)
            else:
                process.wait()
            break
        except KeyboardInterrupt:
            process.send_signal(signal.SIGINT)
        except: raise
    status = process.poll()
    if get_output:
        output = outputf.getvalue()
        outputf.close()
    else: output = None
    return (status, output)

_dryrun = False

def setup(kwargs):
    """
    Configure the process launcher module.
    """
    dryrun = kwargs.get('dryrun', False)

    global _dryrun
    _dryrun = dryrun

def system(cmd, check_status=False, get_output=False, print_output=False,
           output_stderr=False):
    """
    Executes given command.
    Given command can be a string or a list or arguments.
    """
    printable_cmd = cmd
    if isinstance(cmd, list):
        printable_cmd = list2cmdline(cmd)
    if _dryrun:
        logging.info(printable_cmd)
        return get_output and (0, None) or 0
    logging.debug('command [%s]' % printable_cmd)
    root_logger = logging.getLogger()
    debug_mode = root_logger.isEnabledFor(logging.DEBUG)
    quiet_mode = not root_logger.isEnabledFor(logging.INFO)
    print_output = print_output and not quiet_mode
    get_output_ = get_output or debug_mode
    status, output = _subcall(
        cmd, print_output=print_output,
        get_output=get_output_, output_stderr=output_stderr)
    if get_output:
        logging.debug('\n  | ' + '\n  | '.join(output.split('\n')))
        logging.debug('command [%s] -> %s' % (printable_cmd, str(status)))
    if check_status and status: sys.exit(status)
    return get_output and (status, output) or status