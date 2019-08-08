from pygear.lang import struct


@struct
class Message:
    topic_type = "message"
    payload: str

    @property
    def topic_ref(self):
        return ""


@struct
class QueryMessage(Message):
    topic_type = "query"
    query_type: str
    client_id: str

    @property
    def topic_ref(self):
        return self.query_type


@struct
class ResponseMessage(Message):
    topic_type = "response"
    client_id: str

    @property
    def topic_ref(self):
        return self.client_id


@struct
class EventMessage(Message):
    topic_type = "event"
    event_type: str

    @property
    def topic_ref(self):
        return self.event_type