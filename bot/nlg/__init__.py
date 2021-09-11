"""
"""

class Message(object):
    def __init__(self, value, _type="text"):
        self.value = value
        self.type = _type

    def __repr__(self):
        if self.type == "text":
            return self.value
        elif self.type == "image":
            return "image='{}'>".format(self.value)
        elif self.type == "v-card":
            return "contact='{}'>".format(self.value)

class Answer(object):
    def __init__(self, message):
        self.messages = [message]
    
    def add(self, message):
        self.messages.append(message)

    def __repr__(self):
        return "; ".join(map(str, self.messages))

def reply(action, conversation=None):
    return None

class InvalidAction(Exception):
    pass
