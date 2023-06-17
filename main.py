import requests
from bs4 import BeautifulSoup
def send_telegram(text: str):
    token = "6241227464:AAHVt3QBVuB-rL742vvvpFNKOagCiEgAuHk"
    url = "https://api.telegram.org/bot"
    channel_id = "@anekdotiky_ru"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        raise Exception("post_text error")

def get_anekdot(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    text = root.select_one('p')
    for br in text.find_all("br"):
        br.replace_with("\n")
    return text.text

url = 'https://anekdoty.ru/'
anekdot = get_anekdot(url)

if __name__ == '__main__':
  send_telegram(anekdot)