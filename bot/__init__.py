"""
"""
import os
import pickle
# import redis
from datetime import timedelta, datetime
from .conversation import Conversation, Interaction
from .nlu import understand, Intent
from .dm import think
from .nlg import reply
from .config import Config

# r = redis.from_url(url=os.getenv('REDIS_URL'))

CONVERSATION_EXPIRATION_MINUTES = 30.0

class Bot(object):
    def __init__(self, user_id):
        # User interacting with bot
        self.user_id = user_id
        # Bot configuration (TODO)
        self.config = Config(user_id)
        # History of conversations
        # if not self._load_history():
        #     self.history = [Conversation(user_id)]
        self.history = [Conversation(user_id)]
        # Current conversation
        self.conversation = self._current_conversation()

    # def _load_history(self):
    #     hist = r.get(self.user_phone)
    #     if hist:
    #         self.history = pickle.loads(hist)
    #         return True
    #     return False

    def _current_conversation(self):
        if not self.history:
            raise Exception("No conversations found")
        latest = None
        index = 0
        for i, conversation in enumerate(self.history):
            if latest:
                if latest.start_time < conversation.start_time:
                    latest = conversation
                    index = i
            else:
                latest = conversation
                index = i
        # Check if conversation has expired
        if (datetime.now() - latest.start_time).total_seconds() / 60.0 > CONVERSATION_EXPIRATION_MINUTES:
            # If it's expired, return a new conversation
            return Conversation(self.user_phone)
        else:
            # otherwise pop the latest
            return self.history.pop(index)

    def save(self):
        # Add current conversation to history
        self.history.append(self.conversation)
        # Save history
        # r.set(self.user_phone, pickle.dumps(self.history))
        # r.expire(self.user_phone, timedelta(days=1))
        # Other... TODO

    def message(self, query, message_type="text", channel=None):
        interaction = Interaction(query, message_type, channel)
        # NLU
        intent, entities = understand(query, status=self.conversation.status, context=self.conversation.context)
        interaction.intent = intent
        interaction.entities = entities
        # DM & NLG
        answer = self.process_interaction(interaction, intent, entities)
        return answer
    
    def process_interaction(self, interaction, intent, entities):
        # DM
        interaction.status_start = self.conversation.status
        action, self.conversation = think(intent, entities, self.conversation)
        interaction.status_end = self.conversation.status
        interaction.action = action
        # NLG
        answer = reply(action, self.conversation)
        interaction.answer = answer
        self.conversation.interactions.append(interaction)
        print(interaction)
        return answer

    def __repr__(self):
        data = {
            "user_phone": self.user_phone,
            "conversation": self.conversation,
            "history": self.history 
        }
        return str(data)
