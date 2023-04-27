"""
Library to call instances of the OpenDataSoft API
"""

import requests
import time
import logging


class OpenDataSoftAPI:
    DEFAULT_MAX_RETRIES = 5
    DEFAULT_INSTANCE = "https://data.opendatasoft.com"
    DEFAULT_LIMIT = 10
    MAX_LIMIT = 100

    def __init__(
        self, instance: str = DEFAULT_INSTANCE, limit: int = DEFAULT_LIMIT
    ) -> None:
        self.instance = instance.rstrip("/")
        self.set_limit(limit)
        self.max_retries = self.DEFAULT_MAX_RETRIES

    def set_limit(self, limit: int) -> None:
        """
        Set the value of the limit parameter (1-50)
        """
        if not isinstance(limit, int):
            raise ValueError("Error: limit must be an integer between 1 and 100")

        if 0 < limit <= self.MAX_LIMIT:
            self.limit = limit
        elif limit <= 0:
            self.limit = self.DEFAULT_LIMIT
        else:
            self.limit = self.MAX_LIMIT

    def api_call(self, endpoint: str, payload: dict) -> dict:
        """
        Perform a single call on the API, with up to 5 retries if there is an error
        """

        response = requests.get(endpoint, params=payload)
        try:
            retries = self.max_retries
            if response.status_code != 200:
                while retries:
                    logging.warning(f"An error happened, retrying (retries: {retries})")
                    logging.debug("Parameters used:")
                    logging.debug(f"endpoint: {endpoint}")
                    logging.debug(f"payload: {payload}")
                    logging.debug(f"response: {response.text}")
                    time.sleep(5)
                    response = requests.get(endpoint, params=payload)
                    if response.status_code == 200:
                        break
                    else:
                        retries -= 1

            return response.json()
        except KeyError:
            print("An exception occurred while calling the API")
            print(response.__dict__)

    def api_call_loop(self, endpoint: str, payload: dict, results_key: str) -> list:
        """
        Performs a series of calls on the API to get all results when there are several pages
        """
        payload["limit"] = self.limit

        response = self.api_call(endpoint, payload)
        total_count = response["nhits"]

        if total_count > 0:
            results = response[results_key]
            offset = self.limit
            payload["offset"] = offset

            while offset < total_count:
                response = self.api_call(endpoint, payload)
                offset += self.limit
                payload["offset"] = offset

                results.extend(response[results_key])

            return results

        else:
            logging.info("The research returned no (new) results.")
            return []

    def get_records(self, payload: dict) -> dict:
        endpoint = f"{self.instance}/api/records/1.0/search"
        return self.api_call_loop(
            endpoint=endpoint, payload=payload, results_key="records"
        )
