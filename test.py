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

import cal
import conf
import fire
import shell
import slack
import deploy
import doctest
import unittest
import timekeeper
import servicenow

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(cal))
    tests.addTests(doctest.DocTestSuite(conf))
    tests.addTests(doctest.DocTestSuite(shell))
    tests.addTests(doctest.DocTestSuite(slack))
    tests.addTests(doctest.DocTestSuite(deploy))
    tests.addTests(doctest.DocTestSuite(timekeeper))
    tests.addTests(doctest.DocTestSuite(servicenow))
    return tests

def test(verbosity=1):
    verbosity = int(verbosity)
    unittest.main(verbosity=verbosity)

if __name__ == '__main__':
    fire.Fire(test)
