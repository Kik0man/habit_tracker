import requests
from django.conf import settings

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    proxies = {
        'http': 'socks5://localhost:9050',
        'https': 'socks5://localhost:9050'
    }
    data = {'chat_id': chat_id, 'text': text}
    try:
        response = requests.post(url, json=data, proxies=proxies, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return None