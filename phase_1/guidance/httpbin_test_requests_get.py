import requests

# In this example we can make a get request to the httpbin.org with parameters
# The request library can handle with the url creation with no errors
# We could do the url manually but it is more prone to the error
payload = {'page': 25, 'count': 2}

r = requests.get('http://httpbin.org/get', params=payload)

print(r.url)