"""
"""
from typing import Any, List, Literal, Optional
from pydantic import BaseModel
from bot import conversation
from bot.config import BotConfig

from bot.conversation import Conversation, Interaction
from bot.nlu import Intent, understand
from bot.dm import think
from bot.nlg import reply
from bot.nlu.entities import Entity
from bot.utils import LanguageEnum

# r = redis.from_url(url=os.getenv('REDIS_URL'))

CONVERSATION_EXPIRATION_MINUTES = 30.0


class Bot(object):
    def __init__(self, config: BotConfig):
        self.config: BotConfig = config
        self.conversation: Optional[Conversation] = None

    def start_conversation(self, id: str, language: Optional[LanguageEnum] = None, initial_status: Optional[str] = None) -> None:
        self.conversation = Conversation(id=id)
        if initial_status is not None:
            self.conversation.status = initial_status
        if language is not None:
            self.conversation.language = language

    def continue_conversation(self, conversation: Conversation) -> None:
        self.conversation = conversation

    def message(self, query: str):
        print()
        print("+++", query)
        interaction = Interaction(query=query, language=LanguageEnum.SPANISH)
        # NLU
        intent, entities = understand(query, status=self.conversation.status, context=self.conversation.context)
        interaction.intent = intent
        interaction.entities = entities
        print("Understanding...")
        print(intent)
        print(entities)
        # DM & NLG
        answer = self.process_interaction(interaction, intent, entities)
        return answer

    def process_interaction(self, interaction: Interaction, intent: Intent, entities: List[Entity]):
        # DM
        interaction.status_start = self.conversation.status
        action, self.conversation = think(intent, entities, self.conversation)
        print("Thinking...")
        print(action)
        interaction.status_end = self.conversation.status
        interaction.action = action
        # NLG
        answer = reply(self.config, action, self.conversation)
        print("Talking...")
        print("---", answer)
        interaction.answer = answer
        self.conversation.interactions.append(interaction)
        print()
        print(self.conversation.context)
        print()
        return answer

    def __repr__(self):
        data = {
            "user_phone": self.user_phone,
            "conversation": self.conversation,
            "history": self.history 
        }
        return str(data)
