#!/usr/bin/python3.6
import sys
import json
import requests
from pprint import pprint

values = [
    # add to values..
]


def missinglink_sample(values):
    request_json = {
        "values": values,
        "options": {
            "channel": 0
        }
    }

    # list containers
    duplicate_values = list()
    values_container = list(set(request_json['values']))

    if len(request_json['values']) != len(values_container):
        # Check for duplicates in the list of 'values'
        for v in request_json['values']:
            if v in values_container:
                index = values_container.index(v)
                values_container.pop(index)
                continue
            else:
                duplicate_values.append(v)

        if len(duplicate_values) > 0:
            pprint("Duplicate values: ",duplicate_values)
            print("Remove duplicate values in the list of 'values' !")
            sys.exit()

    else:
        # Request 'MissingLink-request' API
        res = requests.post(
            url='http://118.223.123.214:4090/api/missinglink/request',
            data=json.dumps(request_json),
        )

        if res.status_code == 200:
            # Getting JsonResponse
            pprint(res.json())
            return res.json()

        else:
            # Server Error Case
            pprint(res.status_code)
            return res.status_code


if __name__ == "__main__":
    missinglink_sample(values)