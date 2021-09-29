from django.test import TestCase
from amsterdam_app_api.PushNotifications.SendNotification import SendNotification


class TestSendNotification(TestCase):
    def test_send(self):
        send_notification = SendNotification('mock')
        result = send_notification.send()
        self.assertEqual(result, None)
