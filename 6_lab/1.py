import requests

r = requests.get('https://google.com')

print(r.url)
print(r.headers['Content-Type'])
print(r.encoding)
print(r.ok)