import requests
import json

start_datetime_report = '2018-01-01T00:00:00'
end_datetime_report = '2018-01-31T00:00:00'
where = f"(:created_at BETWEEN '{start_datetime_report}' AND '{end_datetime_report}') OR (:updated_at BETWEEN '{start_datetime_report}' AND '{end_datetime_report}')"

params = {
    '$$exclude_system_fields': False,
    '$limit': 9999999999
#    '$where': '(:created_at BETWEEN "'"2023-06-01T00:00:00Z"'" AND "'"2023-06-30T23:59:59Z"'") OR (:updated_at BETWEEN "'"2023-06-01T00:00:00Z"'" AND "'"2023-06-30T23:59:59Z"'")'
}

headers = {
    "X-App-Token": "Ax7ks1Cmr0r6TEssy44yJj4ts",
    "Content-type": "application/json"
}

r = requests.get('https://data.sfgov.org/resource/wg3w-h783.json', 
                            params=params, 
                            headers=headers
)


data = json.dumps(r.json(), indent=4)

print()