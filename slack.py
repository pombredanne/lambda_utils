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

import re
import fire
import requests

def send_message(slack_url, channel, msg):
    response = requests.post(slack_url, json={'channel': '@{}'.format(channel), 'text': msg})
    response.raise_for_status()

def convert_userid_to_real_name(access_token, userid):
    """
    >>> import conf
    >>> sui = conf.load_config('lambda_utils.tst', ['slack_userid'])
    >>> at = conf.load_config('oit-weekly-reports-prd-function', ['slack_access_token'], separator='-')
    >>> real_name = convert_userid_to_real_name(at['slack_access_token'], sui['slack_userid'])
    >>> len(real_name.split(' '))
    2
    >>> convert_userid_to_real_name(at['slack_access_token'], 'U11111111')
    Traceback (most recent call last):
    ...
    Exception: user_not_found: U11111111
    """
    if not isinstance(userid, str):
        userid = userid.group(0)
        userid = userid.replace('<@', '').replace('>', '')
    response = requests.get('https://slack.com/api/users.info?token={}&user={}&pretty=1'.format(access_token, userid))
    response.raise_for_status()
    data = response.json()
    if not data['ok']:
        raise Exception(data['error'] + ": " + userid)
    return data['user']['real_name']

def decode_message(access_token: str, message: str):
    """
    >>> import conf
    >>> config = conf.load_config('lambda_utils.tst', ['slack_encoded_message', 'slack_decoded_message'])
    >>> at = conf.load_config('oit-weekly-reports-prd-function', ['slack_access_token'], separator='-')
    >>> config['slack_decoded_message'] == decode_message(at['slack_access_token'], config['slack_encoded_message'])
    True
    """
    message = re.sub(r'<@(.*?)>', lambda x: convert_userid_to_real_name(access_token, x), message)
    message = re.sub(r'<#.*?\|(.*?)>', r'#\1', message)
    return message


def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
