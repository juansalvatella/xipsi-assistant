import datetime

class Context(object):
    def __init__(self):
        # Context variables that define the flow
        # of the conversation
        pass

class Interaction(object):
    def __init__(self, query, _type, channel):
        self.query = query
        self.type = _type
        self.channel = channel
        self.intent = None
        self.entities = []
        self.action = None
        self.answer = None
        self.status_start = None
        self.status_end = None

    def __repr__(self):
        message = "---------------\n"
        message += self.query + "\n"
        if self.intent:
            message += str(self.intent) + "\n"
        if self.entities:
            message += "[" + ", ".join(map(str, self.entities)) + "]\n"
        if self.status_start and self.status_end:
            message += self.status_start + " -> " + self.status_end + "\n"
        if self.action and self.answer:
            message += "[" + self.action + "] " + str(self.answer)
        return message

class Conversation(object):
    def __init__(self, user_id, channel=None):
        self.user_id = user_id
        self.user = None
        self.type = None
        self.context = Context()
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.channel = channel
        self.interactions = []
        self.status = "start"
