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

import sys
import json
import requests
import conf
from functools import wraps
import byu_ws_sdk as byu_ws
from datetime import datetime

config = conf.load_config('timekeeper', ['api_key', 'shared_secret'])

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

def tk_delete(url, body, actor_net_id):
    return requests.delete(url,
            headers={'Authorization': api_key_header(url, 'DELETE', actor_net_id)},
            data=body)

def create_task(tk_url, description, datestr, actor_net_id):
    return tk_post(tk_url + '/tasks',
            json.dumps({"user": actor_net_id, "description": description, "date": datestr+'T00:10:00.000Z'}),
            actor_net_id)

def get_labor_task(tk_url, work_order, labor_task_name, actor_net_id):
    prefix = work_order.split('-')[0]
    response = tk_get(tk_url + '/laborTaskRelationships?filter={}'.format(prefix),
            actor_net_id)
    if prefix in response.json():
        for task in response.json()[prefix]:
            if task['taskDesc'] == labor_task_name:
                return {'name': task['taskDesc'], 'code': task['taskId']}
    raise Exception("{} is not a valid labor task name for the prefix {}".format(labor_task_name, prefix))

def update_task(tk_url, hours_worked, work_order, actor_net_id, task_id, labor_task):
    """
    It's lame that we can't do this in one call, but the current timekeeper services
    don't work correctly if you try to just call the POST with all the values.
    You have to call create_task above and then this one.
    """
    return tk_put(tk_url + '/tasks/' + task_id,
            json.dumps({'taskid': task_id, 'hours': hours_worked, 'laborTask': labor_task,
             'workOrder': work_order, 'approved': 'false'}),
            actor_net_id)

def import_task(tk_url, description, datestr, actor_net_id):
    response = create_task(tk_url, description, datestr, actor_net_id)
    print(response.text)
    print(response.headers)
    response_body_json = response.json()
    new_task_id = ''
    if 'id' in response_body_json:
        new_task_id = response_body_json['id']
    labor_task = get_labor_task(tk_url, work_order, labor_task_name, actor_net_id)
    return update_task(tk_url, hours_worked, work_order, actor_net_id, new_task_id, labor_task), new_task_id

def import_batch(input_obj_list, actor_net_id):
    return_objs = []
    for task in input_obj_list:
        response, imported_task_id = import_task(task, actor_net_id)
        if response.status_code == 200:
            task['imported_task_id'] = imported_task_id
        return_objs.append(task)
    return return_objs

if __name__ == '__main__':
    fire.Fire()
