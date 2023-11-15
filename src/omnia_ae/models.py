from typing import Optional, TypedDict, Dict, Any
from requests.models import Response
import json

class SourceModel(TypedDict):
    facility: str

class EventModel(TypedDict):
    timestamp: Optional[str]
    sourceName: Optional[str]
    description: Optional[str]
    eventType: Optional[str]
    eventCategory: Optional[str]
    message: Optional[str]
    severity: Optional[int]
    priority: Optional[int]
    condition: Optional[str]
    alarmState: Optional[str]
    ackedState: Optional[bool]
    activeState: Optional[bool]
    suppressedOrShelved: Optional[bool]
    node: Optional[str]
    processArea: Optional[str]
    actionTIme: Optional[str]
    otherField: Optional[Dict[str, Any]]

class SubscriptionModel(TypedDict):
    facility: str

class ConnectionStringModel(TypedDict):
    connectionString: str

class MessageModel(TypedDict):
    statusCode: int
    message: str
    traceId: str

class AERequestFailedException(Exception):
    def __init__(self, response: Response) -> None:
        error = json.loads(response.text)
        self._status_code = response.status_code
        self._reason = response.reason
        self._message = error["message"]
        self._trace_id = error["traceId"] if "traceId" in error else None
        super().__init__(
            f"Status code: {self._status_code}, Reason: {self._reason}, Message: {self._message},  Trace ID: {self._trace_id}")

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def message(self) -> str:
        return self._message

    @property
    def trace_id(self) -> str:
        return self._trace_id
