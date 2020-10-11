import requests
import json
import os

app_id = ''
api_key = ''

def get_jobs(city, num_jobs):
    r = requests.get(f'http://api.adzuna.com/v1/api/jobs/us/search/1?app_id={app_id}&app_key={api_key}&results_per_page=20&content-type=application/json')
    if r.status_code == 200:
        return r.json()


if __name__ == '__main__':
    keys_file = open("keys.txt")
    lines = keys_file.readlines()
    app_id = lines[0].rstrip()
    api_key = lines[1].rstrip()

    r = get_jobs('austin', 20)
    print(json.dumps(r, indent=4, sort_keys=True))

    # print(api_key, app_id)
