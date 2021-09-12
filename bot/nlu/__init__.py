from .entities import Entity, UnitEntity, _extract_angle, _extract_direction, _extract_axis, _extract_distance

class Intent(object):
    def __init__(self, name, confidence=1):
        self.name = name
        self.confidence = confidence

    def __repr__(self):
        return self.name + "(" + str(self.confidence) + ")"

def understand(query, status=None, context=None):
    # Get intents
    intents = _get_intents(query)
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

def _get_intents(query):
    """
    Returns list of intents with confidences
    ["greet", "grasp", "move", "drop", "search", "none"]
    """
    intents = []
    query = clean_query(query)
    # Greet
    if any(word in query for word in ["hola", "ei", "saluda"]):
        intents.append(Intent("greet", 1))
    # Move, Body expressions
    if any(word in query for word in ["mueve", "muévelo", "mover", "desplaza", "acércate", "muévete", "ven", "sube", "baja", "ponte", "avanza", "retrocede"]):
        intents.append(Intent("move", 0.9))
    # Acercate/Ven
    # TODO: Done in "Move"
    # Grasp
    # Drop
    # Search
    if not intents:
        intents.append(Intent("none", 1.0))
    return intents

def _extract_entities(query):
    """
    Returns list of entities
    """
    entities = []
    word_list = clean_query(query)
    # Move, Body expressions
    # i.e. el brazo, la cabeza, ...
    if any(word in word_list for word in ["brazo"]):
        entities.append(Entity("body-part", "arm"))
    # Angles (with direction)
    # i.e. 10 grados, 30 grados a la derecha, ...
    # TODO: Add angle units
    angle = _extract_angle(word_list)
    if angle:
        entities.append(Entity("angle", angle))
    # Directions
    # i.e. derecha, izquierda, ...
    direction = _extract_direction(query)
    if direction:
        entities.append(Entity("direction", direction))
    # Axis (x,y,z)
    axis = _extract_axis(query)
    if axis:
        entities.append(Entity("axis", axis))
    # Distance
    # i.e. 5cm, 5 centimentros, ...
    dist = _extract_distance(word_list)
    if dist:
        # TODO: Add distance units
        entities.append(Entity("distance", dist))

    # Time-directions
    # i.e. a las 6, a las 9, ...
    return entities

def clean_query(query):
    query = query.lower()
    query = query.replace(',', '')
    query = query.replace('.', '')
    query = query.replace("'", ' ')
    query = query.split(' ')
    return query