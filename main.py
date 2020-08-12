import json
import requests
import os
import prettytable
import errno
from datetime import datetime


def get_query_data(state):
    query = 'https://disease.sh/v3/covid-19/states?sort=cases&yesterday=false'
    full_data = (requests.get(query))
    if full_data.status_code == 200:
        json_data = json.loads(full_data.text)

        # return (json_data)
        counter = 0
        for num in json_data:
            if num['state'] == state:
                return json_data[counter]
            counter = counter + 1


if __name__ == "__main__":
    state = 'California'
    data = get_query_data(state)
    print(data)
    output_table = prettytable.PrettyTable([state, ' ', '  '])
    output_table.add_row(['cases', 'deaths', 'active'])
    output_table.add_row([data['cases'], data['deaths'], data['active']])
    print (output_table)
