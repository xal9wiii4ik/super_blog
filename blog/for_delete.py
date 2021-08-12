import requests

from blog.settings import BOT_TOKEN

message_url = f'https://api.telegram.org/bot{BOT_TOKEN}' \
                  f'channels/getFullChannel-1001549508186'
data = {
    'chat_id': '-1001549508186'
}
# -1001549508186
response = requests.post(url=message_url)
print(response.json())
# for res in response.json()['result']:
#     print(res['user']['username'])
