#!/usr/bin/env python
#
# Copyright 2017 Brigham Young University
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
import csv
import sys
import json
import yaml
import fire
import requests
from functools import wraps
import byu_ws_sdk as byu_ws
from datetime import datetime
import conf
import cal

config = conf.load_config('ical2timekeeper.prd', ['ws_url', 'api_key', 'shared_secret'])
test_config = conf.load_config('ical2timekeeper.tst', ['work_order', 'actor'])

# Generic HTTP functions

def api_key_header(url, method, actor_net_id):
    return byu_ws.get_http_authorization_header(
            config['api_key'], config['shared_secret'],
            byu_ws.KEY_TYPE_API, byu_ws.ENCODING_NONCE,
            url=url, actor=actor_net_id, httpMethod=method)

def tk_get(url, actor_net_id):
    return requests.get(url,
            headers={'Authorization':
            api_key_header(url, 'GET', actor_net_id)})

def tk_post(url, body, actor_net_id):
    req = requests.Request('POST', url,
            headers={'Authorization': api_key_header(url, 'POST', actor_net_id),
            'Content-Type': 'application/json'},
            data=body)
    prepared = req.prepare()
    s = requests.Session()
    return s.send(prepared)

def tk_put(url, body, actor_net_id):
    return requests.put(url,
            headers={'Authorization': api_key_header(url, 'PUT', actor_net_id),
            'Content-Type': 'application/json'},
            data=body)

def tk_delete(url, actor_net_id):
    return requests.delete(url,
            headers={'Authorization': api_key_header(url, 'DELETE', actor_net_id)})

# Timekeeper domain functions

def get_labor_task(work_order, labor_task_name, actor_net_id):
    """
    >>> {'code': u'PRO', 'name': u'Professional Development'} == get_labor_task(test_config['work_order'], 'Professional Development', test_config['actor'])
    True
    """
    prefix = work_order.split('-')[0]
    response = tk_get(config['ws_url'] + '/laborTaskRelationships?filter={}'.format(prefix),
            actor_net_id)
    if prefix in response.json():
        for task in response.json()[prefix]:
            if task['taskDesc'] == labor_task_name:
                return {'name': task['taskDesc'], 'code': task['taskId']}
    raise Exception("{} is not a valid labor task name for the prefix {}".format(labor_task_name, prefix))

def get_task(task_id, actor_net_id):
    response = tk_get(config['ws_url'] + '/tasks/' + task_id, actor_net_id)
    return response

def get_tasks(actor_net_id, start_date, end_date):
    """
    >>> response = get_tasks(test_config['actor'], '2017-04-08', '2017-04-14')
    >>> response.status_code
    200
    >>> len(response.json()) > 1
    True
    >>> 'description' in response.json()[0].keys()
    True
    """
    response = tk_get(config['ws_url'] + '/tasks?netid={}&startDate={}&endDate={}'.format(actor_net_id, start_date, end_date), actor_net_id)
    return response

def create_task(description, datestr, actor_net_id):
    response = tk_post(config['ws_url'] + '/tasks',
            json.dumps({"user": actor_net_id, "description": description,
             "date": datestr+'T00:10:00.000Z'}),
            actor_net_id)
    return response

def update_task(hours_worked, work_order, actor_net_id, task_id, labor_task):
    """
    It's lame that we can't do this in one call, but the current timekeeper services
    don't work correctly if you try to just call the POST with all the values.
    You have to call create_task above and then this one.
    """
    response = tk_put(config['ws_url'] + '/tasks/' + task_id,
            json.dumps({'taskid': task_id, 'hours': hours_worked, 'laborTask': labor_task,
             'workOrder': work_order, 'approved': 'false'}),
            actor_net_id)
    return response

def delete_task(task_id, actor_net_id):
    response = tk_delete(config['ws_url'] + '/tasks/' + task_id, actor_net_id)
    response.raise_for_status()

def import_task(description, hours_worked, datestr, work_order, labor_task_name, actor_net_id):
    """
    >>> response, task_id = import_task('test task', '0.1', datetime.now().strftime('%Y-%m-%d'), test_config['work_order'], 'Professional Development', test_config['actor'])
    >>> delete_task(task_id, test_config['actor'])
    """
    response = create_task(description, datestr, actor_net_id)
    response.raise_for_status()
    response_body_json = response.json()
    new_task_id = ''
    if 'id' in response_body_json:
        new_task_id = response_body_json['id']
    labor_task = get_labor_task(work_order, labor_task_name, actor_net_id)
    response = update_task(hours_worked, work_order, actor_net_id, new_task_id, labor_task)
    return response, new_task_id

def parse_file(file_name):
    """
    >>> [item for item in parse_file('test_input.csv')]
    [['crazy friday', '8.0', 'AA-111-1: Crazy Friday', 'Project Meetings'], ['oit singers weekly get together', '0.5', 'OH-11111-1: Overhead Labor', 'Other']]
    """
    with open(file_name, 'r') as csvfile:
        for row in csv.reader(csvfile):
            yield row

def import_file(file_name, actor_net_id, date_str):
    for row in parse_file(file_name):
        import_row(row, actor_net_id, date_str)
        
def import_row(row, actor_net_id, date_str=""):
    print('This is one entry that will be imported: ' + str(row))
    description, hours_worked, work_order, labor_task_name = row
    if not date_str:
        date_str = cal.last_friday_str()
    response, task_id = import_task(description, hours_worked, date_str, work_order, labor_task_name, actor_net_id)
    num_retries=1
    max_retries=5
    while response.status_code != 200 and num_retries <= max_retries:
        print('failed with response code {}, retrying {} of {}'.format(response.status_code, num_retries, max_retries))
        response, task_id = import_task(description, hours_worked, date_str, work_order, labor_task_name, actor_net_id)
        num_retries += 1
    if response.status_code != 200:
        print(response.text)
        print('after {} retries we still failed.  Response code: {}'.format(max_retries, response.status_code))
        sys.exit(1)
    else:
        print('imported successfully')

def test(verbose=False):
    import doctest
    doctest.testmod(verbose=verbose)

if __name__ == '__main__':
    fire.Fire()
