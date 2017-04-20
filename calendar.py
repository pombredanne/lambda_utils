#!/usr/bin/env python
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
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta, SA

def date_str_2_obj(date_str):
    """
    >>> date_str_2_obj('2017-01-01')
    datetime.datetime(2017, 1, 1, 0, 0)
    """
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def get_last_saturday_str():
    """
    >>> response = get_last_saturday_str()
    >>> date_str_2_obj(response).strftime('%a')
    'Sat'
    >>> date_str_2_obj(response) <= datetime.datetime.today()
    True
    """
    return (datetime.datetime.now() + relativedelta(weekday=SA(-1))).strftime('%Y-%m-%d')

def timedelta_2_hours(duration):
    """
    >>> timedelta_2_hours(datetime.timedelta(hours=1))
    1
    """
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds / 3600.0
    return round(hours, 3)

def calc_duration(start_date_str, end_date_str):
    return timedelta_2_hours(parser.parse(end_date_str) - parser.parse(start_date_str))

def add_days_to_date_str(date_str, num_days):
    """
    >>> add_days_to_date_str('2017-01-01', 2)
    '2017-01-03'
    >>> add_days_to_date_str('2017-01-01', -2)
    '2016-12-30'
    """
    date_obj = parser.parse(date_str)
    new_date = date_obj + datetime.timedelta(days=num_days)
    return new_date.strftime('%Y-%m-%d')

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
