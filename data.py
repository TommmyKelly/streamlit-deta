import requests
import config



url = 'https://database.deta.sh/v1/a0fnubft/example-db/items'

headers = {'X-API-Key': config.key,
           'Content-Type': 'application/json'}
data = {
    "item": {
        
        'age': '23',
        'name': 'private'
       
    }
}
print(data)

res = requests.post(url, headers=headers, json=data)

print(res.headers)

print(res.text)

