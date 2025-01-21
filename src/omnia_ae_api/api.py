from typing import Literal, Optional
from azure.identity._internal.msal_credentials import MsalCredential

from omnia_ae_api.http_client import HttpClient, ContentType
from omnia_ae_api.models import SourceModel, EventModel, SubscriptionModel, MessageModel, ConnectionStringModel

AeVersion = Literal["1"]

class Environment:
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
    def Test(cls, version: AeVersion = "1"):
        return cls(
            resource_id="657b2767-ee47-47ff-b745-af501ea053cb",
            base_url=f"https://api-test.gateway.equinor.com/iiot/ae/v{version}"
        )

    @classmethod
    def Prod(cls, version: AeVersion = "1"):
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


class API:
    """
    Wrapper class for interacting with the Omnia Industrial IIoT Alarm & Events API.
    For more information, see https://github.com/equinor/OmniaPlant/wiki or consult with the Omnia IIoT team.
    Args:
        :param azure_credential: Azure credential instance used for authenticating
        :type azure_credential: MsalCredential

        :param environment: API deployment environment
        :type environment: Environment
    """

    def __init__(self, azure_credential: MsalCredential, environment: Environment):
        self._http_client = HttpClient(
            azure_credential=azure_credential, resource_id=environment.resource_id)
        self._base_url = environment.base_url.rstrip('/')

    def get_sources(self) -> SourceModel:
        """https://api.equinor.com/api-details#api=iiot-ae-api-v1&operation=GetSources"""
        return self._http_client.request(request_type='get', url=f"{self._base_url}/sources", payload=None, params=None)
    
    def get_events(
            self, 
            facility: str,
            sourceName: str = "*", 
            limit: int = 10, 
            startTime: Optional[str] = None,
            endTime: Optional[str] = None,
            sort: Optional[str] = None,
            includeOtherFields: Optional[bool] = None,
            description: Optional[str] = None,
            eventType: Optional[str] = None,
            eventCategory: Optional[str] = None,
            message: Optional[str] = None,
            severity: Optional[int] = None,
            priority: Optional[int] = None,
            condition: Optional[str] = None,
            alarmState: Optional[str] = None,
            ackedState: Optional[bool] = None,
            activeState: Optional[bool] = None,
            suppressedOrShelved: Optional[bool] = None,
            node: Optional[str] = None,
            processArea: Optional[str] = None,
            actiontime: Optional[str] = None,
            continuationToken: Optional[str] = None,
            accept: ContentType = "application/json") -> EventModel:
        """
        https://api.equinor.com/api-details#api=iiot-ae-api-v1&operation=GetEvents
        Default: sourceName *, limit = 10
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
        if description is not None:
            params['description'] = description
        if eventType is not None:
            params['eventType'] = eventType
        if eventCategory is not None:
            params['eventCategory'] = eventCategory
        if message is not None:
            params['message'] = message
        if severity is not None:
            params['severity'] = severity
        if priority is not None:
            params['priority'] = priority
        if condition is not None:
            params['condition'] = condition
        if alarmState is not None:
            params['alarmState'] = alarmState
        if ackedState is not None:
            params['ackedState'] = ackedState
        if activeState is not None:
            params['activeState'] = activeState
        if suppressedOrShelved is not None:
            params['suppressedOrShelved'] = suppressedOrShelved
        if node is not None:
            params['node'] = node
        if processArea is not None:
            params['processArea'] = processArea
        if actiontime is not None:
            params['actiontime'] = actiontime
        if continuationToken is not None:
            params['continuationToken'] = continuationToken
        
        return self._http_client.request(
            request_type='get',
            url=f"{self._base_url}/events/{facility}",
            accept=accept,
            params=params
        )

    def get_routing_subscriptions(self) -> SubscriptionModel:
        """https://api.equinor.com/api-details#api=iiot-ae-api-v1&operation=GetSubscriptions"""
        return self._http_client.request(
            request_type='get',
            url=f"{self._base_url}/streaming/subscriptions"
        )

    def set_realtime_subscription(
            self, 
            connectionString,
            ) -> MessageModel:
        """https://api.equinor.com/api-details#api=iiot-ae-api-v1&operation=SetRealTimeDestination"""
        request: ConnectionStringModel = {"ConnectionString": connectionString}
        return self._http_client.request(
            request_type='post',
            url=f"{self._base_url}/streaming/destination",
            payload=request
        )
    
    def create_subscription(
            self, 
            facility: str,
            ) -> MessageModel:
        """https://api.equinor.com/api-details#api=iiot-ae-api-v1&operation=CreateSubscriptions"""
        return self._http_client.request(
            request_type='post',
            url=f"{self._base_url}/streaming/subscriptions/{facility}"
        )
    
    def delete_subscription(
            self, 
            facility: str,
            ) -> MessageModel:
        """https://api.equinor.com/api-details#api=iiot-ae-api-v1&operation=DeleteSubscription"""
        return self._http_client.request(
            request_type='delete',
            url=f"{self._base_url}/streaming/subscriptions/{facility}"
        )