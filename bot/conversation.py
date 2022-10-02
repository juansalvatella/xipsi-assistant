from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from bot.master import Master

from bot.utils import LanguageEnum
from bot.nlu.entities import Entity

class Context(BaseModel):
    speaker_name: Optional[str] = None
    master_recognized: Optional[Master] = None

class Interaction(BaseModel):
    query: str
    language: LanguageEnum
    intent: Optional[str] = None
    entities: List[Entity] = []
    action: Optional[str] = None
    answer: Optional[str] = None
    status_start: Optional[str] = None
    status_end: Optional[str] = None

    # def __repr__(self):
    #     message = "---------------\n"
    #     message += self.query + "\n"
    #     if self.intent:
    #         message += str(self.intent) + "\n"
    #     if self.entities:
    #         message += "[" + ", ".join(map(str, self.entities)) + "]\n"
    #     if self.status_start and self.status_end:
    #         message += self.status_start + " -> " + self.status_end + "\n"
    #     if self.action and self.answer:
    #         message += "[" + self.action + "] " + str(self.answer)
    #     return message

class Conversation(BaseModel):
    id: str
    context: Context = Context()
    start_time: datetime = datetime.now()
    end_time: Optional[datetime] = None
    interactions: List[Interaction] = []
    status: str = "START"
    language: LanguageEnum = LanguageEnum.SPANISH
