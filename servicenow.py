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

import fire
import conf
import requests

def get(sn_url, username, password):
    """
    >>> sn = conf.load_config('servicenow.tst', ['url'])
    >>> user = conf.load_config('servicenow.prd', ['username', 'password'])
    >>> rows = get(sn['url'], user['username'], user['password'])
    >>> len(rows) > 1
    True
    >>> all(['sys_id' in row for row in rows])
    True
    """
    result = []
    response = requests.get(sn_url, auth=(username, password))
    response.raise_for_status()
    result = response.json()['result']
    return result

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
