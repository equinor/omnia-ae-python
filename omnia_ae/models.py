from typing import List, Optional, TypedDict, Dict, Any, Literal
from requests.models import Response
import json

class SourceModel(TypedDict):
    facility: str

