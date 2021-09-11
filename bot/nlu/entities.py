class Entity(object):
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __repr__(self):
        message = "Entity(" + self.name
        if self.value:
            message += ", \"" + self.value + "\""
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

class Proposal(Entity):
    def __init__(self, producer=None, price=None, image=None):
        super().__init__("proposal")
        self.producer = producer
        self.price = price
        self.image = image

    def __repr__(self):
        return  "Entity(" + self.name + ", \"producer=" + str(self.producer.username) + ",price=" + str(self.price) + ",image=" + str(self.image) + "\"" + ")"

def _is_weight_unit(word):
    unit = False
    if word in ['kilo', 'quilo', 'kg', 'kilos', 'quilos', 'kgs']:
        unit = 'kg'
    elif word in ['gram', 'grams']:
        unit = 'g'
    elif word in ['capsa', 'caixa', 'capses', 'caixes']:
        unit = 'box'
    elif word in ['bossa', 'bosses']:
        unit = 'bag'
    elif word in ['dotzena', 'dotzenes']:
        unit = 'unit'
    return unit

def _is_distance_unit(word):
    unit = False
    if word in ["m", "metres", "metre"]:
        unit = "m"
    if word in ["kms", "km", "kilometre", "quilometre", "quilometres"]:
        unit = "km"
    return unit

def _is_fraction(word):
    fraction = {}
    if word in ['mig', 'mitja']:
        #fraction['text'] = word
        #fraction['value'] = 0.5
        fraction = word
    elif word in ['terç']:
        #fraction['text'] = word
        #fraction['value'] = 0.33
        fraction = word
    return fraction

def _is_amount(word):
    amount = False
    if word in ['un','una','1']:
        amount = 1
    elif word in ['dos','dues','parell','2']:
        amount = 2
    elif word in ['tres','3']:
        amount = 3
    elif word in ['quatre','4']:
        amount = 4
    elif word in ['cinc','5']:
        amount = 5
    elif word in ['sis','6']:
        amount = 6
    elif word in ['set','7']:
        amount = 7
    elif word in ['vuit','8']:
        amount = 8
    elif word in ['nou','9']:
        amount = 9
    elif word in ['deu','10']:
        amount = 10
    elif word in ['onze','11']:
        amount = 11
    elif word in ['dotze','dotzena','dotzenes','12']:
        amount = 12
    elif word in ['tretze','13']:
        amount = 13
    elif word in ['catorze','14']:
        amount = 14
    elif word in ['quinze','15']:
        amount = 15
    elif word in ['setze','16']:
        amount = 16
    elif word in ['disset','17']:
        amount = 17
    elif word in ['divuit','18']:
        amount = 18
    elif word in ['dinou','19']:
        amount = 19
    elif word in ['vint','20']:
        amount = 20
    elif word in ['vintiu','vintiun','vint-i-un','21']:
        amount = 21
    elif word in ['vintidos','vint-i-dos','22']:
        amount = 22
    elif word in ['vintitres','vint-i-tres','23']:
        amount = 23
    elif word in ['vintiquatre','vint-i-quatre','24']:
        amount = 24
    return amount

def extract_other(query):
    entities = []
    # Delivery
    if "a recollir" in query:
        entities.append(Entity(name="delivery", value="takeaway"))
    return entities
