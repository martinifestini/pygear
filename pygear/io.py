import abc
import typing
import functools


class Converter(abc.ABC):
    @abc.abstractmethod
    def serialize(self, obj) -> str:
        pass

    @abc.abstractmethod
    def deserialize(self, s, obj_type):
        pass


class IOInterface(abc.ABC):
    converter: Converter

    def __init__(self, converter: Converter):
        self.converter = converter

    def send(self, target: typing.Callable, payload):
        target(
            self.converter.serialize(payload)
        )

    def receive(self, serialized_payload):
        return self.converter.deserialize(serialized_payload)