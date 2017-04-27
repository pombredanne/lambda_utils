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
from base64 import b64decode
import conf
import shell

kms = boto3.client('kms')

def deploy(profile, install_deps=False, extra_files=[]):
    """
    No automated tests as we don't want to deploy on each test run
    """
    config = conf.load_config('lambda', ['upload_s3_bucket'])
    shell.shell('mkdir -p deploy')
    shell.shell('cp *.py *.yml requirements.txt deploy/')
    for f in extra_files:
        shell.shell('cp {} deploy/'.format(f))
    os.chdir('deploy')
    if install_deps:
        shell.shell('pip install -r requirements.txt -t .')
    shell.shell('aws cloudformation package --template-file sam_pre.yml --output-template-file sam_post.yml --s3-bucket {} --profile {}'.format(config['upload_s3_bucket'], profile))
    shell.shell('aws cloudformation deploy --template-file sam_post.yml --stack-name SLA-weekly-report --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --profile {}'.format(profile))
    os.chdir('..')

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
