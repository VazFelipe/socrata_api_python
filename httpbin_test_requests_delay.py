import requests

# in this example we have used the delay route and return an exception when the response delay is greater than the timeout
r = requests.get('https://httpbin.org/delay/6', timeout=3, verify=False)

print(r.status_code)