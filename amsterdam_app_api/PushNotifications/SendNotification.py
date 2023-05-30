""" Send pushnotification """
import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
from amsterdam_app_api.GenericFunctions.Logger import Logger
from amsterdam_app_api.models import Notification
from amsterdam_app_api.models import FollowedProjects
from amsterdam_app_api.models import FirebaseTokens
from amsterdam_app_backend.settings import BASE_DIR


class SendNotification:
    """ Send notification through the firebase network (google) """
    def __init__(self, identifier, batch_size=500):
        self.logger = Logger()
        self.identifier = identifier
        self.batch_size = batch_size
        if not firebase_admin._apps:
            cred = credentials.Certificate('{base_dir}/fcm_credentials.json'.format(base_dir=BASE_DIR))
            self.default_app = firebase_admin.initialize_app(cred)
        else:
            self.default_app = firebase_admin.get_app()

        self.subscribed_device_batches = None
        self.notification = None
        self.project_identifier = None
        self.article_type = None
        self.link_source_id = None
        self.setup_result = self.setup()
        self.valid_notification = self.setup_result['status']

    def setup(self):
        """ Init subscribers """
        self.notification = self.set_notification()
        if self.notification is None or self.article_type is None:
            return {'status': False, 'result': 'No notification or article type found'}

        self.subscribed_device_batches = self.create_subscribed_device_batches()
        if len(self.subscribed_device_batches) == 0:
            return {'status': False, 'result': 'No subscribed devices found'}

        return {'status': True, 'result': 'valid notification'}

    def set_notification(self):
        """ Set notification object """
        try:
            notification = Notification.objects.filter(pk=self.identifier).first()
            self.project_identifier = notification.project_identifier_id
            if notification.news_identifier != '' and notification.news_identifier is not None:
                self.article_type = 'NewsUpdatedByProjectManager'
                self.link_source_id = notification.news_identifier
            elif notification.warning_identifier != '' and notification.warning_identifier is not None:
                self.article_type = 'ProjectWarningCreatedByProjectManager'
                self.link_source_id = notification.warning_identifier

            return messaging.Notification(
                title=notification.title,
                body=notification.body
            )
        except Exception as error:
            self.logger.error('Caught error in SendNotification.set_notification(): {error}'.format(error=error))
            return None

    def create_subscribed_device_batches(self):
        """ Create batches of subscribers """
        followers = [x.deviceid for x in list(FollowedProjects.objects.filter(projectid=self.project_identifier).all())]
        filtered_devices = [x.firebasetoken for x in list(FirebaseTokens.objects.filter(deviceid__in=followers).all())]
        return [filtered_devices[x:x + self.batch_size] for x in range(0, len(filtered_devices), self.batch_size)]

    def send_multicast_and_handle_errors(self):
        """ Send message to subscribers """

        # Only send the notification if the setup() went well
        if self.valid_notification is False:
            return

        failed_tokens = []
        for registration_tokens in self.subscribed_device_batches:
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
