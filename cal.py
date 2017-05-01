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
import datetime
from dateutil.relativedelta import relativedelta, SA, FR

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

def last_friday_str():
    """
    >>> output = last_friday_str()
    >>> len(output) == 10
    True
    >>> output.startswith('2')
    True
    >>> date_str_2_obj(output) < datetime.datetime.now()
    True
    >>> date_str_2_obj(output).strftime('%a')
    'Fri'
    """
    last_friday = datetime.datetime.now() + relativedelta(weekday=FR(-1))
    return last_friday.strftime('%Y-%m-%d')

def timedelta_2_hours(duration):
    """
    >>> timedelta_2_hours(datetime.timedelta(hours=1))
    1.0
    """
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds / 3600.0
    return round(hours, 3)
    
def parse_date_str(date_str):
    """
    >>> parse_date_str('2017-01-01')
    datetime.datetime(2017, 1, 1, 0, 0)
    """
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')
    
def parse_datetime_str(date_str):
    """
    >>> parse_datetime_str('2017-01-01T11:30:00.000-0600')
    datetime.datetime(2017, 1, 1, 11, 30, tzinfo=datetime.timezone(datetime.timedelta(-1, 64800)))
    """
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.000%z')

def calc_duration(start_date_str, end_date_str):
    """
    returns the duration in hours between 2 date strings
    >>> calc_duration('2017-01-01T11:30:00.000-0600', '2017-01-02T11:34:00.000-0600')
    24.067
    """
    return timedelta_2_hours(parse_datetime_str(end_date_str) - parse_datetime_str(start_date_str))

def add_days_to_date_str(date_str, num_days):
    """
    >>> add_days_to_date_str('2017-01-01', 2)
    '2017-01-03'
    >>> add_days_to_date_str('2017-01-01', -2)
    '2016-12-30'
    """
    date_obj = parse_date_str(date_str)
    new_date = add_days_to_date(date_obj, num_days)
    return new_date.strftime('%Y-%m-%d')

def add_days_to_date(date_obj, num_days):
    """
    >>> add_days_to_date(datetime.datetime(2017, 1, 1), 2)
    datetime.datetime(2017, 1, 3, 0, 0)
    """
    return date_obj + datetime.timedelta(days=num_days)

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
