""" Send pushnotification """
import firebase_admin
from firebase_admin import credentials, messaging

from construction_work.generic_functions.generic_logger import Logger
from construction_work.generic_functions.static_data import DEFAULT_NOTIFICATION_BATCH_SIZE
from construction_work.models import Device
from main_application.settings import BASE_DIR

logger = Logger()


class NotificationService:
    """Send notification through the firebase network (google)"""

    def __init__(self, notification_object, batch_size=DEFAULT_NOTIFICATION_BATCH_SIZE):
        self.notification_object = notification_object
        self.batch_size = batch_size
        if not firebase_admin._apps:
            cred = credentials.Certificate("{base_dir}/fcm_credentials.json".format(base_dir=BASE_DIR))
            self.default_app = firebase_admin.initialize_app(cred)
        else:
            self.default_app = firebase_admin.get_app()

        self.subscribed_device_batches = None
        self.firebase_notification = None
        self.setup_result = None

    def setup(self):
        """Init subscribers"""
        self.firebase_notification = messaging.Notification(
            title=self.notification_object.title, body=self.notification_object.body
        )

        self.subscribed_device_batches = self.create_subscribed_device_batches()
        if len(self.subscribed_device_batches) == 0:
            self.setup_result = "No subscribed devices found"
            return False
        return True

    def create_subscribed_device_batches(self):
        """Create batches of subscribers"""
        project_id = self.notification_object.warning.project.pk
        # devices = list(Device.objects.filter(followed_projects__=project_id).all())

        devices = self.notification_object.warning.project.device_set.all()
        if not devices.exists():
            return []
        firebase_tokens = [x.firebase_token for x in devices]
        return [firebase_tokens[x : x + self.batch_size] for x in range(0, len(firebase_tokens), self.batch_size)]

    def send_multicast_and_handle_errors(self):
        """Send message to subscribers"""
        failed_tokens = []
        for registration_tokens in self.subscribed_device_batches:
            message = messaging.MulticastMessage(
                data={
                    "linkSourceid": str(self.notification_object.warning.pk),
                    "type": "ProjectWarningCreatedByProjectManager",
                },
                notification=self.firebase_notification,
                tokens=registration_tokens,
            )

            response = messaging.send_each_for_multicast(message)
            if response.failure_count > 0:
                responses = response.responses
                for idx, resp in enumerate(responses):
                    if not resp.success:
                        # The order of responses corresponds to the order of the registration tokens.
                        failed_tokens.append(registration_tokens[idx])

        # Log result
        logger.error("List of tokens that caused failures: {0}".format(failed_tokens))
