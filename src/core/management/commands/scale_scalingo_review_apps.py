import json
import logging
import requests

from django.conf import settings
from django.core.management.base import BaseCommand


logger = logging.getLogger(__name__)

SCALINGO_API_ENDPOINT = "https://api.osc-fr1.scalingo.com/v1/apps"
API_HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    # 'Authorization': f'Bearer {settings.SCALINGO_API_TOKEN_BEARER}'
}
REVIEW_APP_NAME_PREFIX = "aides-terr-staging-pr"
SCALING_DIRECTION_DEFAULT = "down"  # 'up'


class Command(BaseCommand):
    """
    Commands to scale up or down the Scalingo Review Apps.

    Scalingo API doc ? https://developers.scalingo.com/

    Steps:
    1. Get the bearer token
    2. Get the list of Review Apps
    3. Scale up or down the Review Apps

    Usage:
    python manage.py scale_scalingo_review_apps up
    python manage.py scale_scalingo_review_apps down
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "direction",
            nargs=1,
            type=str,
            default=SCALING_DIRECTION_DEFAULT,
            help="The scaling direction. up or down.",
        )

    def handle(self, *args, **options):
        direction = options["direction"][0]
        logger.info(f"Starting to scale {direction} the Scalingo Review Apps")

        # update API headers
        SCALINGO_API_TOKEN_BEARER = self.get_scalingo_bearer_token()
        API_HEADERS["Authorization"] = f"Bearer {SCALINGO_API_TOKEN_BEARER}"

        current_review_apps = self.get_current_review_apps()
        self.scale_review_apps(current_review_apps, direction)

    def get_scalingo_bearer_token(self):
        """The bearer token expires every hour."""
        endpoint = "https://auth.scalingo.com/v1/tokens/exchange"
        res = requests.post(
            endpoint, headers=API_HEADERS, auth=("", settings.SCALINGO_API_TOKEN)
        )  # noqa
        data = res.json()
        return data["token"]

    def get_current_review_apps(self):
        current_review_apps = []

        # query Scalingo API
        res = requests.get(SCALINGO_API_ENDPOINT, headers=API_HEADERS)
        if res.status_code == 200:
            data = res.json()

            # filter on review apps
            for app in data["apps"]:
                if app["name"].startswith(REVIEW_APP_NAME_PREFIX):
                    current_review_apps.append(app["name"])

        return current_review_apps

    def scale_review_apps(self, app_names, direction=SCALING_DIRECTION_DEFAULT):  # noqa
        web_amount = 1 if direction == "up" else 0
        data = {"containers": [{"name": "web", "amount": web_amount}]}

        for app_name in app_names:
            endpoint = f"{SCALINGO_API_ENDPOINT}/{app_name}/scale"
            res = requests.post(
                endpoint, headers=API_HEADERS, data=json.dumps(data)
            )  # noqa
            data = res.json()
            logger.info(f"Scaled {direction} Review App {app_name}")
