from .entities import UnitEntity, extract_other

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
    if any(word in query for word in ["hola", "ei"]):
        intents.append(Intent("greet", 1))
    # Move
    if any(word in query for word in ["mueve", "mover", "desplaza", "acércate", "muévete", "ven"]):
        intents.append(Intent("greet", 0.9))
    # Acercate/Ven
    # TODO: Done in "Move"
    # Grasp
    # Drop
    # Search
    return [Intent("none", 1)]

def clean_query(query):
    query = query.lower()
    query = query.replace(',', '')
    query = query.replace('.', '')
    query = query.replace("'", ' ')
    query = query.split(' ')
    return query

def _extract_entities(query):
    """
    Returns list of entities
    """
    entities = []
    return entities
