from typing import List, Literal, Optional
from azure.identity._internal.msal_credentials import MsalCredential

from typing import Literal, Optional, TypedDict, Union, Dict, Any
from azure.identity._internal.msal_credentials import MsalCredential
import requests
import logging
from omnia_ae.http_client import HttpClient, ContentType
from omnia_ae.models import SourceModel
#from omnia_timeseries.helpers import retry
#from omnia_timeseries.models import TimeseriesRequestFailedException
from importlib import metadata
from opentelemetry.instrumentation.requests import RequestsInstrumentor
import platform
#from omnia_ae import AEAPI, AEEnvironment

AeVersion = Literal["1.0"]

class AEEnvironment:
    def __init__(self, resource_id: str, base_url: str):
        self._resource_id = resource_id
        self._base_url = base_url

    @classmethod
    def Dev(cls, version: AeVersion = "1"):
        return cls(
            resource_id="657b2767-ee47-47ff-b745-af501ea053cb",
            base_url=f"https://api-dev.gateway.equinor.com/iiot/ae/v{version}"
        )

    @classmethod
    def Test(cls, version: AeVersion = "1.0"):
        return cls(
            resource_id="657b2767-ee47-47ff-b745-af501ea053cb",
            base_url=f"https://api-test.gateway.equinor.com/iiot/ae/v{version}"
        )

    @classmethod
    def Prod(cls, version: AeVersion = "1.0"):
        return cls(
            resource_id="6df18f43-f499-4470-9d94-52b01698620d",
            base_url=f"https://api.gateway.equinor.com/iiot/ae/v{version}"
        )

    @property
    def resource_id(self) -> str:
        return self._resource_id

    @property
    def base_url(self) -> str:
        return self._base_url


class AEAPI:
    """
    Wrapper class for interacting with the Omnia Industrial IIoT AE API.
    For more information, see https://github.com/equinor/OmniaPlant/wiki or consult with the Omnia IIoT team.
    Args:
        :param azure_credential: Azure credential instance used for authenticating
        :type azure_credential: MsalCredential

        :param environment: API deployment environment
        :type environment: AEEnvironment
    """

    def __init__(self, azure_credential: MsalCredential, environment: AEEnvironment):
        self._http_client = HttpClient(
            azure_credential=azure_credential, resource_id=environment.resource_id)
        self._base_url = environment.base_url.rstrip('/')

    def get_sources(self, accept: ContentType = "application/json") -> SourceModel:
        return self._http_client.request(request_type='get', url=self._base_url+'/sources', accept='application/json', payload=None, params=None)
    
    def get_events(
            self, 
            facility: str,
            sourceName: str = "*", 
            limit: int = 10, 
            startTime: Optional[str] = None,
            endTime: Optional[str] = None,
            sort: Optional[str] = None,
            includeOtherFields: Optional[bool] = None,
            accept: ContentType = "application/json"):
        """
        Default: soruceName *, limit = 10
        """
        params = {}
        if startTime is not None:
            params['startTime'] = startTime
        if endTime is not None:
            params['endTime'] = endTime
        if includeOtherFields is not None:
            params['includeOtherFields'] = includeOtherFields
        if sort is not None:
            params['sort'] = sort
        if limit is not None:
            params['limit'] = limit
        if sourceName is not None:
            params['sourceName'] = sourceName
        return self._http_client.request(
            request_type='get',
            url=f"{self._base_url}/events/{facility}",
            accept=accept,
            params=params
        )

