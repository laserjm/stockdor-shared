from enum import Enum
from pydantic import BaseModel

class JobStates(str, Enum):
    queued = "queued"
    accepted = "accepted"
    finished = "finished"
    error = "error"