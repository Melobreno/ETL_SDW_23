import pandas as pd 
import requests
import json
import openai

sdw2023_url = 'https://sdw-2023-prd.up.railway.app'
openai_api_key = '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'

df = pd.read_csv('SDW23.CSV')
user_ids = df['UserID'].tolist()
print(user_ids)

def get_User(id):
  response = requests.get(f'{sdw2023_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_User(id)) is not None]

print(json.dumps(users, indent=2))

openai.api_key = openai_api_key

def gerenate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-Turbo",
    messages=[
    {
        "role": "system",
        "content": "Você é um especialista em marketing bancário."
    },
    {
        "role": "user",
        "content": f"Crie uma mensagem para {user['name']}! sobre as importancias dos investimentos. (maximo de 100 caracteres)"
    }
  ]
)
  return completion.choices[0].message.content.strip('\"')
for user in users:
  news = gerenate_ai_news(user)
  print(news)
  user['news'].append({
    "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/pay.svg",
    "description": news
    })
  
def update_user(user):
    response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")