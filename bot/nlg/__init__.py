from enum import Enum
from bot.core import BotConfig

from bot.conversation import Conversation

class ActionEnum(str, Enum):
    GREET = "GREET"
    MEET_MASTER = "MEET_MASTER"
    NOT_UNDERSTAND = "NOT_UNDERSTAND"
    ASK_NAME = "ASK_NAME"
    NICE_TO_MEET_YOU = "NICE_TO_MEET_YOU"

def reply(config: BotConfig, action: ActionEnum, conversation: Conversation) -> str:
    if action == ActionEnum.GREET:
        return "¡Hola! Encantado"
    elif action == ActionEnum.MEET_MASTER:
        return "¿Eres mi maestro?"
    elif action == ActionEnum.ASK_NAME:
        return f"Me llamo {config.name}, y tu?"
    elif action == ActionEnum.NICE_TO_MEET_YOU:
        return f"Pues encantado de conocerte {conversation.context.speaker_name}"
    return "No te he entendido"


def _greet(conversation: Conversation) -> str:
    if conversation.context.master_recognized is not None:
        speaker_name = conversation.context.master_recognized.name
    else:
        speaker_name = "plebeyo"
    return f"Hola {speaker_name}! Encantado de saludarte de nuevo"


class InvalidAction(Exception):
    pass
