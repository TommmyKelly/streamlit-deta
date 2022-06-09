import requests
import config
import pandas as pd



url = 'https://database.deta.sh/v1/a0fnubft/example-db/query'

headers = {'X-API-Key': config.key,
           'Content-Type': 'application/json'}
data = {
    "item": {
        
        'age': '23',
        'name': 'private'
       
    }
}
print(data)

res = requests.post(url, headers=headers)

print(res.json()['items'])

df = pd.DataFrame(res.json()['items'])

print(df.head)

df.to_csv('data.csv',index=False, sep=';')

