import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
from amsterdam_app_api.GenericFunctions.Logger import Logger
from amsterdam_app_api.models import MobileDevices
from amsterdam_app_api.models import Notification
from amsterdam_app_backend.settings import BASE_DIR


class SendNotification:
    def __init__(self, identifier, batch_size=500):
        self.logger = Logger()
        self.identifier = identifier
        self.batch_size = batch_size
        if not firebase_admin._apps:
            cred = credentials.Certificate('{base_dir}/fcm-credentials.json'.format(base_dir=BASE_DIR))
            self.default_app = firebase_admin.initialize_app(cred)
        else:
            self.default_app = firebase_admin.get_app()

        self.subscribed_device_batches = None
        self.notification = None
        self.project_identifier = None
        self.article_type = None  # news, warning
        self.link_source_id = None
        self.valid_notification = self.setup()

    def setup(self):
        self.notification = self.set_notification()
        if self.notification is None or self.article_type is None:
            return False

        self.subscribed_device_batches = self.create_subscribed_device_batches()
        if len(self.subscribed_device_batches) == 0:
            return False

        return True

    def set_notification(self):
        try:
            notification = Notification.objects.filter(pk=self.identifier).first()
            self.project_identifier = notification.project_identifier
            if notification.news_identifier != '' and notification.news_identifier is not None:
                self.article_type = 'NewsUpdatedByProjectManager'
                self.link_source_id = notification.news_identifier
            elif notification.warning_identifier != '' and notification.warning_identifier is not None:
                self.article_type = 'WarningCreatedByProjectManager'
                self.link_source_id = notification.warning_identifier

            return messaging.Notification(
                title=notification.title,
                body=notification.body
            )
        except Exception as error:
            self.logger.error('Caught error in SendNotification.set_notification(): {error}'.format(error=error))
            return None

    def create_subscribed_device_batches(self):
        filtered_devices = list(MobileDevices.objects.filter(projects__contains=[self.project_identifier]))
        return [filtered_devices[x:x + self.batch_size] for x in range(0, len(filtered_devices), self.batch_size)]

    def send_multicast_and_handle_errors(self):
        # Only send the notification if the setup() went well
        if self.valid_notification is False:
            return

        failed_tokens = []
        for batch in self.subscribed_device_batches:
            registration_tokens = [x.device_token for x in batch]
            message = messaging.MulticastMessage(
                data={'linkSourceid': str(self.link_source_id), 'type': self.article_type},
                notification=self.notification,
                tokens=registration_tokens,
            )

            response = messaging.send_multicast(message)
            if response.failure_count > 0:
                responses = response.responses
                for idx, resp in enumerate(responses):
                    if not resp.success:
                        # The order of responses corresponds to the order of the registration tokens.
                        failed_tokens.append(registration_tokens[idx])

        # Log result
        self.logger.error('List of tokens that caused failures: {0}'.format(failed_tokens))
