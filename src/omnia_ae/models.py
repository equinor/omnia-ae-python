from typing import List, Optional, TypedDict, Dict, Any, Literal
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