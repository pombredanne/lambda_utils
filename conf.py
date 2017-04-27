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
import os
import fire
import yaml
import boto3
import tempfile

s3 = boto3.resource('s3')
kms = boto3.client('kms')

config_var_names = []
def load_config(file_name):
    """
    >>> config_var_names = ['a', 'b', 'c']
    >>> config = load_config('test.yml') # test locally running
    >>> all([key in config.keys() for key in config_var_names])
    True
    """
    if 'RUNNING_IN_LAMBDA' in os.environ:
        config = decrypt_s3_vars(file_name)
    else:
        with open(file_name) as fobj:
            config = yaml.load(fobj.read())
    return config

def decrypt_s3_vars(secrets_bucket_name, file_name):
    obj = s3.Object(secrets_bucket_name, file_name)
    encrypted_value = obj.get()['Body'].read()
    kmsresponse = kms.decrypt(CiphertextBlob=b64decode(encrypted_value))
    return yaml.load(kmsresponse['Plaintext'])

def encrypt_vars_to_s3(profile):
    """
    This method is run locally to encrypt the config files' values into a timekeeper_alerter.yml file in s3
    """
    with tempfile.NamedTemporaryFile() as tfile:
        yaml.dump(config, tfile)
        tfile.flush()
        encrypted_value = _output('aws kms encrypt --key-id {} --plaintext fileb://{} --output text --query CiphertextBlob --profile {}'.format(config['kms_key_arn'], tfile.name, profile))
    with tempfile.NamedTemporaryFile() as tfile:
        tfile.write(encrypted_value)
        tfile.flush()
        _shell('aws s3 cp {} s3://{}/timekeeper_alerter.yml --profile {}'.format(tfile.name, config['secrets_bucket_name'], profile))

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
