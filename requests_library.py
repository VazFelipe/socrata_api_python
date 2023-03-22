import requests

# request from https://xkcd.com/353/
# for image download use https://imgs.xkcd.com/comics/python.png
r = requests.get("https://imgs.xkcd.com/comics/python.png", verify=False)

# this snippet downloads the image from r into the projectTest folder
# with open('comic.png', 'wb') as f:
#     f.write(r.content)

# dir() returns the attributes and methods from the r response
# help() returns more details about the r response
# r.content returns the content in bytes
# staus_code 200=success, 300=redirects, 400=client errors (permission to do), 500=server errors (permission to do)  
# ok returns True if the status_code is different then 400 or 500, otherwise False
print(r.headers)

for header in r.headers:
    # if not header.find('X'):
    print(header)

