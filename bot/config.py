from pydantic import BaseModel
from typing import List
from bot.master import Master

class BotConfig(BaseModel):
    name: str
    masters: List[Master] = []
