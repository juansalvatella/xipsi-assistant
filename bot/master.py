from pydantic import BaseModel
from typing import Optional, Literal, Any

class Master(BaseModel):
    name: Optional[str] = None
    gender: Literal["MALE", "FEMALE", "FLUID"] = "MALE"
    preferred_courtesy_name: str = "mi lord"
    formal_speech: bool = True
    face: Optional[Any] = None # TODO: Something to recognize face
