#!/usr/bin/env python3.6
# Copyright 2016 Brigham Young University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function
import fire
import subprocess

def output(cmd):
    """
    >>> output('echo "testing"')
    b'testing\\n'
    """
    return subprocess.check_output(cmd, shell=True)

def shell(cmd):
    """
    >>> shell('echo ""')
    Running \"echo \"\"\"...
    """
    print('Running "{}"...'.format(cmd))
    subprocess.check_call(cmd, shell=True)

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
