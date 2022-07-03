import time

import requests

URL = 'http://127.0.0.1:5000'


response = requests.post(f'{URL}/mailing/', json={"body": "some text"})
print(response.status_code)
if response.ok:
    print(response.json())

task_id = response.json()['task_id']

response = requests.get(f'{URL}/mailing/{task_id}')
print(response.status_code)
if response.ok:
    print(response.json())

time.sleep(2)
response = requests.get(f'{URL}/mailing/{task_id}')
print(response.status_code)
if response.ok:
    print(response.json())

