import requests

# In this example we make a request to the htpbin.org and post some data as a payload
payload = {'username': 'vaz', 'password': 'testing'}

r = requests.post('https://httpbin.org/post', data=payload, verify=False)

# we have used the r.text method and it return a json from the r response
# instead of doing this we could use r.json() and parse the text return into a dictionary

r_dict = r.json()

print(r_dict)