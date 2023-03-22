import requests

# in this example we have used the basic-auth route and tested the authentication on httpbin.org
r = requests.get('https://httpbin.org/basic-auth/vaz/testing', auth=('vaz', 'testing'), verify=False)

print(r)