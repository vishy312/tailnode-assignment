import requests

res = requests.get('https://dummyapi.io/data/v1/user/60d0fe4f5311236168a109ca/post', headers={'app-id': '62568ae89312b5a8218a8b53'})

print(res.json())