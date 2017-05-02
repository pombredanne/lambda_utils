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

import os
import fire
import yaml
import boto3
import tempfile

def connect_ssm(profile=''):
    """
    >>> ssm = connect_ssm()
    """
    if profile:
        session = boto3.Session(profile_name=profile)
        ssm = session.client('ssm')
    else:
        ssm = boto3.client('ssm')
    return ssm

def load_config(prefix, var_names, profile=''):
    """
    >>> config = load_config('test.tst', ['a', 'b', 'c'])
    >>> config['a']
    '1'
    >>> config['b']
    'b'
    >>> config['c']
    'three'
    """
    ssm = connect_ssm(profile)
    config = {}
    response = ssm.get_parameters(Names=[prefix + '.' + name for name in var_names], WithDecryption=True)
    for parameter in response['Parameters']:
        config[parameter['Name'].replace(prefix+'.','')] = parameter['Value']
    return config

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
