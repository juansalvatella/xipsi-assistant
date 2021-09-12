import re

#TODO: Add pint library https://pint.readthedocs.io/en/stable/

DISTANCE_UNIT = "(metros|m)"
DISTANCE_UNIT_E1 = "(decametros|dm)"
DISTANCE_UNIT_E2 = "(hectometros|hm)"
DISTANCE_UNIT_E3 = "(kilometros|km|kms)"
DISTANCE_UNIT_NE1 = "(decimetros|dm)"
DISTANCE_UNIT_NE2 = "(centimetros|cm|cms)"
DISTANCE_UNIT_NE3 = "(milimetros|mm|mms)"
DISTANCE_REGEX = "(" + DISTANCE_UNIT + "|" + DISTANCE_UNIT_E1 + "|" + DISTANCE_UNIT_E2 + "|" + DISTANCE_UNIT_E3 + "|" + DISTANCE_UNIT_NE1 + "|" + DISTANCE_UNIT_NE2 + "|" + DISTANCE_UNIT_NE3 + ")"

DIRECTION_X_POS = "(derecha)"
DIRECTION_X_NEG = "(izquierda)"
DIRECTION_Y_POS = "(adelante|avanza)"
DIRECTION_Y_NEG = "(atrás|retrocede)"
DIRECTION_Z_POS = "(arriba|sube)"
DIRECTION_Z_NEG = "(abajo|baja)"

AXIS_X = "(" + DIRECTION_X_NEG + "|" + DIRECTION_X_POS + ")"
AXIS_Y = "(" + DIRECTION_Y_NEG + "|" + DIRECTION_Y_POS + ")"
AXIS_Z = "(" + DIRECTION_Z_NEG + "|" + DIRECTION_Z_POS + ")"

DIRECTION_POS = "(" + DIRECTION_X_POS + "|" + DIRECTION_Y_POS + "|" + DIRECTION_Z_POS + ")"
DIRECTION_NEG = "(" + DIRECTION_X_NEG + "|" + DIRECTION_Y_NEG + "|" + DIRECTION_Z_NEG + ")"

class Entity(object):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __repr__(self):
        message = "Entity(" + self.name
        if self.value:
            message += ", \"" + str(self.value) + "\""
        return  message + ")"

class UnitEntity(Entity):
    def __init__(self, *args, amount=1, units=None):
        super().__init__(*args)
        self.amount = amount
        self.units = units

    def __repr__(self):
        return  "Entity(" + self.name + ", \"" + str(self.amount) + self.units + "\"" + ")"

class Location(Entity):
    def __init__(self, latitude=None, longitude=None, address=None):
        super().__init__("location")
        self.latitude = latitude
        self.longitude = longitude
        self.address = address

    def __repr__(self):
        return  "Entity(" + self.name + ", \"lat=" + str(self.latitude) + ",lon=" + str(self.longitude) + "\"" + ")"

def _is_weight_unit(word):
    unit = False
    if word in ["kilo", "quilo", "kg", "kilos", "quilos", "kgs"]:
        unit = "kg"
    elif word in ["gram", "grams"]:
        unit = "g"
    elif word in ["capsa", "caixa", "capses", "caixes"]:
        unit = "box"
    elif word in ["bossa", "bosses"]:
        unit = "bag"
    elif word in ["dotzena", "dotzenes"]:
        unit = "unit"
    return unit

def _is_distance_unit(word):
    unit = False
    if word in ["m", "metros", "metro"]:
        unit = "m"
    if word in ["kms", "km", "kilometro", "quilometro", "quilometros"]:
        unit = "km"
    return unit

def _is_fraction(word):
    fraction = {}
    if word in ["medio", "media"]:
        #fraction["text"] = word
        #fraction["value"] = 0.5
        fraction = word
    elif word in ["tercio", "tercera"]:
        #fraction["text"] = word
        #fraction["value"] = 0.33
        fraction = word
    return fraction

def _get_amount(word):
    amount = None
    if word in ["nada", "ninguno", "ninguna", "sin"]:
        amount = 0
    if word in ["un", "uno", "una", "1"]:
        amount = 1
    elif word in ["dos", "par", "2"]:
        amount = 2
    elif word in ["tres", "3"]:
        amount = 3
    elif word in ["cuatro", "4"]:
        amount = 4
    elif word in ["cinco", "5"]:
        amount = 5
    elif word in ["seis", "6"]:
        amount = 6
    elif word in ["siete", "7"]:
        amount = 7
    elif word in ["ocho", "8"]:
        amount = 8
    elif word in ["nueve", "9"]:
        amount = 9
    elif word in ["diez", "10"]:
        amount = 10
    elif word in ["once", "11"]:
        amount = 11
    elif word in ["doce", "docena", "docenas", "12"]:
        amount = 12
    elif word in ["trece", "13"]:
        amount = 13
    elif word in ["catorce", "14"]:
        amount = 14
    elif word in ["quince", "15"]:
        amount = 15
    elif word in ["dieciseis", "16"]:
        amount = 16
    elif word in ["diecisiete", "17"]:
        amount = 17
    elif word in ["dieciocho", "18"]:
        amount = 18
    elif word in ["diecinueve", "19"]:
        amount = 19
    elif word in ["veinte", "20"]:
        amount = 20
    elif word in ["veintiuno", "21"]:
        amount = 21
    elif word in ["veintidos", "22"]:
        amount = 22
    elif word in ["veintitres", "23"]:
        amount = 23
    elif word in ["veinticuatro", "24"]:
        amount = 24
    elif word in ["veinticinco", "25"]:
        amount = 25
    return amount

# Movement (units, direction)
# Axis ()

def _extract_angle(word_list):
    query = " ".join([word.replace(word, str(_get_amount(word))) if _get_amount(word) else word for word in word_list])
    # Detect if there is an angle
    m = re.search(r"^(?:.*)(?: )(\d+)( grados)", query)
    if m:
        return m.group(1)

def _extract_distance(word_list):
    query = " ".join([word.replace(word, str(_get_amount(word))) if _get_amount(word) else word for word in word_list])
    # Detect if there is an angle
    m = re.search(r"^(?:.*)(?: )(\d+)( {})".format(DISTANCE_REGEX), query)
    if m:
        return m.group(1)

def _extract_axis(query):
    m = re.search(AXIS_X, query)
    if m:
        return "X"
    m = re.search(AXIS_Y, query)
    if m:
        return "Y"
    m = re.search(AXIS_Z, query)
    if m:
        return "Z"

def _extract_direction(query):
    m = re.search(DIRECTION_POS, query)
    if m:
        return 1
    m = re.search(DIRECTION_NEG, query)
    if m:
        return -1


def extract_other(query):
    entities = []
    # Delivery
    if "a recollir" in query:
        entities.append(Entity(name="delivery", value="takeaway"))
    return entities
