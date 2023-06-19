import requests
from bs4 import BeautifulSoup
import os
import datetime

def send_message_telegram(text: str):
    channel_id = os.environ.get("CHAT_ID")
    token = os.environ.get("TOKEN")
    url = "https://api.telegram.org/bot" + token
    method = url + "/sendMessage"
    data = {
        "chat_id": channel_id,
        "text": text
    }
    r = requests.post(method, data=data)
    if r.status_code != 200:
        raise Exception("post_text_messages error")

def send_photo_telegram(photo, caption):
    channel_id = os.environ.get("CHAT_ID")
    token = os.environ.get("TOKEN")
    url = "https://api.telegram.org/bot" + token
    method = url + "/sendPhoto"
    photo = photo.replace('60', '200x305')
    data = {
        'chat_id': channel_id,
        'photo': photo,
        'caption': caption,
        'parse_mode': 'HTML'}
    r = requests.get(method, params=data)
    if r.status_code != 200:
        raise Exception("post_text_photo error")

def get_anekdot(url):
    rs = requests.get(url)
    soup = BeautifulSoup(rs.content, 'html.parser')
    text = soup.select_one('p')
    for br in text.find_all("br"):
        br.replace_with("\n")
    return text.text

def get_quote(url):
    rs = requests.get(url)
    soup = BeautifulSoup(rs.content, 'html.parser')
    quote = soup.select_one("div[class*=lenta-card]")
    img = quote.select_one("img")['src']
    result = [text for text in quote.stripped_strings] + [img]
    return result

if __name__ == '__main__':
    now = datetime.datetime.now()
    if now.hour % 2 == 0:
        url_book = 'https://www.livelib.ru/quote/random'
        text_book = get_quote(url_book)
        caption = "<b>Книга:</b> {}\n<b>Автор:</b> {}\n<b>Оценка:</b> {}\n<b>Цитата:</b> {}\n".format(text_book[-4], text_book[-3], text_book[-2], ' '.join(map(str, text_book[-5::-1])))
        send_photo_telegram(text_book[-1], caption)
    else:
        url_anekdot = 'https://anekdoty.ru/'
        text_anekdot = get_anekdot(url_anekdot)
        send_message_telegram(text_anekdot)
