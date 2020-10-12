import requests
import json
import os
import pandas

app_id = ''
api_key = ''


def get_jobs(state, county, city, num_jobs):
    state = '&location1=' + state.replace(' ', '%20') if not pandas.isnull(state) else ''
    county = '&location2=' + county.replace(' ', '%20') if not pandas.isnull(county) else ''
    city = '&location3=' + city.replace(' ', '%20') if not pandas.isnull(city) else ''

    req_url = f'http://api.adzuna.com/v1/api/jobs/us/search/1?app_id={app_id}&app_key={api_key}&location0=us{state}{county}{city}&results_per_page={num_jobs}&content-type=application/json'

    r = requests.get(req_url)

    if r.status_code == 200:
        return r.json()
    else:
        return None

if __name__ == '__main__':
    keys_file = open("keys.txt")
    lines = keys_file.readlines()
    app_id = lines[0].rstrip()
    api_key = lines[1].rstrip()

    jobs = pandas.DataFrame()

    cities = pandas.read_csv('./usCities.csv')
    for i, row in cities.iterrows():
        cn = row['City Name']
        print(f'Processing: {cn}')
        r = get_jobs(row['State'], row['County'], row['City'], 10)
        if r:
            results = r["results"]
            for result in results:
                result['company'] = result['company']['display_name']
                result['category'] = result['category']['label']
                result['city'] = row['City Name']
                result['state'] = row['State']
            df = pandas.DataFrame(results)
            if not 'contract_type' in df:
                df['contract_type'] = "Not specified"
            if not 'contract_time' in df:
                df['contract_time'] = "Not specified"
            df = df[['id', 'created', 'company', 'title', 'category', 'description', 'city', 'state', 'latitude', 'longitude', 'contract_type', 'contract_time', 'redirect_url']]
            jobs = jobs.append(df)

    jobs.to_csv('./jobs.csv', index=False)