import abc
import collections
import json
import logging
import typing

from pygear.io import Converter
from pygear.lang import struct, asdict
from . import types

logger = logging.getLogger()


class Dispatcher(abc.ABC):
    @abc.abstractmethod
    def register(self, topic: str, func: typing.Callable):
        pass
    
    @abc.abstractmethod
    def emit(self, topic: str, payload: str):
        pass

    @abc.abstractmethod
    def wait(self, topic: str):
        pass


class MemoryDispatcher(Dispatcher):
    __slots__ = ('_registry')
    
    def __init__(self):
        self._registry: typing.Dict[str, set] = collections.defaultdict(set)

    def __getitem__(self, topic) -> set:
        return self._registry[topic]

    def register(self, topic: str, func: typing.Callable):
        b: set = self[topic]
        b.add(func)
    
    def emit(self, topic: str, payload: str):
        logger.info("asd")
        if topic not in self._registry:
            self._registry[topic].add(payload)
        for func in self[topic]:
            if not isinstance(func, str):
                logger.info(f"Executing {func}")
                func(payload)
        
    def wait(self, topic):
        reg: set = self[topic]
        for payload in reg:
            if isinstance(payload, str):
                reg.remove(payload)
                return payload


@struct
class MessageBus:
    dispatcher: Dispatcher
    json_encoder: json.JSONEncoder = json.JSONEncoder

    def serialize(self, message):
        return json.dumps(
            asdict(message),
            cls=self.json_encoder
        )

    def deserialize(self, s: str, message_type):
        # TODO: attr.structure
        return message_type(**json.loads(s))
    
    def generate_topic(self, topic_type: str, topic_ref: str) -> str:
        return "{}:{}".format(topic_type, topic_ref)

    def publish(self, message: types.Message):
        print(message)
        payload = self.serialize(message)
        topic = self.generate_topic(
            message.topic_type,
            message.topic_ref
        )
        logging.info(f"Emitting to topic {topic}")
        self.dispatcher.emit(
            topic,
            payload
        )
    
    def query(self, query_message: types.QueryMessage) -> types.ResponseMessage:
        self.publish(query_message)
        return self.deserialize(
            self.dispatcher.wait(
                self.generate_topic(
                    "response",
                    query_message.client_id
                )
            ),
            types.ResponseMessage
        )
    
    def subscribe(self, 
                  message_type: types.Message,
                  topic_ref: str,
                  message_handler: typing.Callable):
        logging.info(f"subscribing {message_handler} to {topic_ref}")
        def _subscriber(payload: str):
            message = self.deserialize(payload, message_type)
            logger.info(f"Sending {message} to {message_handler}")
            response = message_handler(message)
            if isinstance(response, types.ResponseMessage):
                self.publish(response)
        topic = self.generate_topic(
            message_type.topic_type,
            topic_ref
        )
        self.dispatcher.register(
            topic,
            _subscriber
        )