from django.test import TestCase
from unittest.mock import patch, MagicMock
from tg_bot.bot import send_telegram_message

class BotTest(TestCase):
    @patch('tg_bot.bot.requests.post')
    def test_send_telegram_message(self, mock_post):
        # Настраиваем мок
        mock_response = MagicMock()
        mock_response.json.return_value = {'ok': True}
        mock_post.return_value = mock_response

        # Вызываем функцию
        result = send_telegram_message(123, 'Hello')

        # Проверяем, что requests.post был вызван с правильными параметрами
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['chat_id'], 123)
        self.assertEqual(kwargs['json']['text'], 'Hello')
        # Можно также проверить, что функция вернула ожидаемый результат
        self.assertEqual(result, {'ok': True})