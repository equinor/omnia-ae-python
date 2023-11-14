from typing import Optional, TypedDict, Dict, Any

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