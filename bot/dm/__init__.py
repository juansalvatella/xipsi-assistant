from typing import List, Tuple
from bot.conversation import Conversation
from bot.nlu import EntityEnum, Intent, IntentEnum
from bot.nlu.entities import Entity
from bot.nlg import ActionEnum
from enum import Enum

class StatusEnum(str, Enum):
    START = "START"
    EXPECTING_NAME = "EXPECTING_NAME"

def think(intent: Intent, entities: List[Entity], conversation: Conversation) -> Tuple[ActionEnum, Conversation]:
    if intent.name == IntentEnum.GREET:
        return ActionEnum.GREET, conversation
    if conversation.status == StatusEnum.START:
        if intent.name == IntentEnum.ASK_NAME:
            conversation.status = StatusEnum.EXPECTING_NAME
            return ActionEnum.ASK_NAME, conversation
    elif conversation.status == StatusEnum.EXPECTING_NAME:
        name_entity = [entity for entity in entities if entity.name == EntityEnum.NAME]
        if name_entity:
            conversation.context.speaker_name = name_entity[0].value
        conversation.status = StatusEnum.START
        return ActionEnum.NICE_TO_MEET_YOU, conversation
    return ActionEnum.NOT_UNDERSTAND, conversation
