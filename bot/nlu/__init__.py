from typing import List, Optional
from pydantic import BaseModel
from .entities import Entity, _extract_angle, _extract_direction, _extract_axis, _extract_distance, _extract_name
from enum import Enum

class IntentEnum(str, Enum):
    GREET = "GREET"
    MOVE = "MOVE"
    NONE = "NONE"
    CONFIRM = "CONFIRM"
    REJECT = "REJECT"
    ASK_NAME = "ASK_NAME"

class EntityEnum(str, Enum):
    BODY_PART = "BODY_PART"
    ANGLE = "ANGLE"
    DIRECTION = "DIRECTION"
    AXIS = "AXIS"
    DISTANCE = "DISTANCE"
    NAME = "NAME"

class Intent(BaseModel):
    name: str
    confidence: float = 1.0

def understand(query: str, status=None, context=None):
    # Get intents
    intents = sorted(_get_intents(query), key=lambda x: x.confidence, reverse=True)
    entities = _extract_entities(query)
    if status or context:
        # Apply business rules according to the context
        # and status to select the most likely intent
        # TODO
        intent = intents[0]
    else:
        # Otherwise get the one
        # with the higher confidence
        intent = intents[0]
    return intent, entities

def _get_intents(query) -> List[Intent]:
    """
    Returns list of intents with confidences
    ["greet", "grasp", "move", "drop", "search", "none"]
    """
    intents = []
    clean_query = get_clean_query(query)
    clean_query_word_list = get_clean_word_list(query)
    # Greet
    if any(word in clean_query_word_list for word in ["hola", "ei", "saluda"]):
        intents.append(Intent(name=IntentEnum.GREET, confidence=1))
    # Move, Body expressions
    if any(word in clean_query_word_list for word in ["mueve", "muévelo", "mover", "desplaza", "acércate", "muévete", "ven", "sube", "baja", "ponte", "avanza", "retrocede"]):
        intents.append(Intent(name=IntentEnum.MOVE, confidence=0.9))
    # Acercate/Ven
    # TODO: Done in "Move"
    # Grasp
    # Drop
    # Search

    # Ask name
    if any(word in clean_query for word in ["te llamas", "tu nombre"]):
        intents.append(Intent(name=IntentEnum.ASK_NAME, confidence=0.9))
    # Confirmation and Rejection
    for intent_method in [_confirmation, _rejection]:
        intent = intent_method(query)
        if intent.confidence > 0.5:
            intents.append(intent)
    if not intents:
        intents.append(Intent(name=IntentEnum.NONE, confidence=1.0))
    return intents

def _confirmation(query: str) -> Intent:
    query = get_clean_query(query)
    intent = Intent(name=IntentEnum.CONFIRM)
    query = query.replace("vale pues", "")
    length = len(query)
    if query in ["lo veo", "sí", "bien", "top", "tops", "vale", "vale va", "que vale", "ok", "okay"]:
        intent.confidence = 0.99
        return intent
    if any(word in query.split() for word in ["mal", "fatal", "no", "nada"]):
        intent.confidence = 0
        return intent
    if any(word in query.split() for word in ["sí", "confirmo", "confirmado", "autorizo"]) and length < 20:
        intent.confidence = 0.85
        return intent
    word_list_single = [
        "bien",
        "exacto",
        "claro",
        "cierto",
        "autorizo",
        "firmoo",
        "confirmo",
        "confirmar",
        "confirmado",
        "confirmada",
        "confirma",
        "afirmativo",
        "verdadero",
        "perfectamente",
        "perfecto",
        "efecto",
        "correcto",
        "genial",
        "estupendo",
        "fantastico",
        "dale",
        "guay",
        "corrector",
    ]
    if any(word == query for word in word_list_single):
        intent.confidence = 0.99
        return intent
    if "puede ser" in query and length < 12:
        intent.confidence = 0.9
        return intent
    word_list_multiple = [
        "pero bien",
        "me da bien",
        "lo veo bien",
        "que sí",
        "eso es",
        "por supuesto",
        "va bien",
        "esta bien",
        "de locos",
        "venga va",
        "de acuerdo",
        "parece bien",
        "me va de lujo",
        "chachi piruli",
        "vale venga",
    ]
    if any(word == query for word in word_list_multiple):
        intent.confidence = 0.99
        return intent
    if any(word in query.split() for word in word_list_single):
        if length < 20:
            intent.confidence = 0.6
            return intent
        if length < 80:
            intent.confidence = 0.5
            return intent
        intent.confidence = 0.3
        return intent
    if any(word in query for word in word_list_multiple):
        if length < 20:
            intent.confidence = 0.6
            return intent
        if length < 80:
            intent.confidence = 0.5
            return intent
        intent.confidence = 0.3
        return intent
    if query.split().count("sí") >= 2:
        intent.confidence = 0.85
        return intent
    intent.confidence = 0.0
    return intent

def _rejection(query: str) -> Intent:
    query = get_clean_query(query)
    intent = Intent(name=IntentEnum.REJECT)
    if query in ["ninguno", "ninguna"]:
        intent.confidence = 0.8
        return intent
    if " o no" in query:
        query = query.replace(" o no", "")
    if query.startswith("no quiero"):
        intent.confidence = 0.8
        return intent
    if query.startswith("no confirmo"):
        return 0.8
    length = len(query)
    if query.split().count("no") > 2:
        intent.confidence = 0.3
        return intent
    if any(word in query.split() for word in ["no", "mal", "fatal", "nada", "complicado", "dificil"]):
        if length < 20:
            intent.confidence = 0.85
            return intent
    word_list = [
        "no quiero",
        "no confirmo",
        "ya estaria",
        "tendria que pensar",
        "negativo",
        "no me va bien",
        "no lo veo",
        "no puedo",
        "me va mal",
        "eso era todo",
        "eso es todo",
        "ya esta",
        "nada mas",
    ]
    if query in word_list:
        intent.confidence = 0.99
        return intent
    if any(word in query for word in word_list):
        if length < 10:
            intent.confidence = 0.85
            return intent
        if length < 30:
            intent.confidence = 0.3
            return intent
    intent.confidence = 0.0
    return intent


def _extract_entities(query):
    """
    Returns list of entities
    """
    entities = []
    word_list = get_clean_word_list(query)
    # Move, Body expressions
    # i.e. el brazo, la cabeza, ...
    if any(word in word_list for word in ["brazo"]):
        entities.append(Entity(name=EntityEnum.BODY_PART, value="arm"))
    # Angles (with direction)
    # i.e. 10 grados, 30 grados a la derecha, ...
    # TODO: Add angle units
    angle = _extract_angle(word_list)
    if angle:
        entities.append(Entity(name=EntityEnum.ANGLE, value=angle))
    # Directions
    # i.e. derecha, izquierda, ...
    direction = _extract_direction(query)
    if direction:
        entities.append(Entity(name=EntityEnum.DIRECTION, value=direction))
    # Axis (x,y,z)
    axis = _extract_axis(query)
    if axis:
        entities.append(Entity(name=EntityEnum.AXIS, value=axis))
    # Distance
    # i.e. 5cm, 5 centimentros, ...
    dist = _extract_distance(word_list)
    if dist:
        # TODO: Add distance units
        entities.append(Entity(name=EntityEnum.DISTANCE, value=dist))

    name = _extract_name(word_list)
    if name:
        entities.append(Entity(name=EntityEnum.NAME, value=name))

    # Time-directions
    # i.e. a las 6, a las 9, ...
    return entities

def get_clean_query(query: str) -> str:
    query = query.lower()
    query = query.replace(",", "")
    query = query.replace(".", "")
    query = query.replace("'", " ")
    query = query.replace("?", "")
    query = query.replace("!", "")
    return query

def get_clean_word_list(query: str) -> List[str]:
    return get_clean_query(query).split(" ")