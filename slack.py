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
import requests

def send_message(slack_url, channel, msg):
    response = requests.post(slack_url, json={'channel': '@{}'.format(channel), 'text': msg})
    response.raise_for_status()

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
