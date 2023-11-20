import unittest
import requests_mock
import pytest
from azure.identity._internal.msal_credentials import MsalCredential
from azure.core.credentials import AccessToken
from requests.models import Response
from omnia_ae_api import API, Environment
from omnia_ae_api.models import RequestFailedException


class DummyCredentials(MsalCredential):

    def get_token(self, *scopes, **kwargs):
        return AccessToken("dummytoken", 0)

    def _get_app(self):
        return None


@pytest.fixture
def api():
    env = Environment("dummy", "https://test")
    api = API(DummyCredentials("dummy"), env)
    return api


def test_retry_on_failure(api):
    with requests_mock.Mocker() as m:
        #m.register_uri("GET", "https://api-dev.gateway.equinor.com/iiot/ae/v1/events/ABC?limit=10&sourceName=%2A", status_code=503,  # 503 is retryable
        m.register_uri("GET", "https://test/events/ABC", status_code=503,  # 503 is retryable
                       text="""{"message": "Service is unavailable", "traceId": "1"}""")
        with pytest.raises(RequestFailedException):
            api.get_events("ABC")
    assert m.call_count == 3, "Unexpected number of retries"


def test_skip_retry_when_not_retryable_status_code(api):
    with requests_mock.Mocker() as m:
        #m.register_uri("GET", "https://api-dev.gateway.equinor.com/iiot/ae/v1/events/ABC?limit=10&sourceName=%2A", status_code=403,  # 403 is not retryable
        m.register_uri("GET", "https://test/events/ABC", status_code=403,  # 403 is not retryable
                       text="""{"message": "Service is unavailable", "traceId": "1"}""")
        with pytest.raises(RequestFailedException):
            api.get_events("ABC")
    assert m.call_count == 1, "Unexpected number of retries"