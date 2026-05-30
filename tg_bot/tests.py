from django.test import TestCase
from unittest.mock import patch, MagicMock
from tg_bot.bot import send_telegram_message

class BotTest(TestCase):
    @patch('tg_bot.bot.bot')
    def test_send_telegram_message(self, mock_bot):
        mock_bot.send_message = MagicMock()
        send_telegram_message(123, 'Hello')
        mock_bot.send_message.assert_called_once_with(chat_id=123, text='Hello')