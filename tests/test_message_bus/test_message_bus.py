from pygear.message_bus import Dispatcher, MemoryDispatcher, MessageBus, types


class MockedDispatcher(Dispatcher):
    _func = None
    _topic = None
    _result = None

    def register(self, topic, func):
        self._func = func
            
    def emit(self, topic, payload):
        self._result = self._func(payload)
    
    def wait(self, topic):
        return self._result


def _handle(message):
    assert message.payload == "a"
    if not hasattr(message, "client_id"):
        return
    return types.ResponseMessage(
        payload="b",
        client_id=message.client_id

    )


def test_message_bus_event():
    dispatcher = MockedDispatcher()
    dispatcher._topic = "event:foo"
    message_bus = MessageBus(dispatcher)
    message_bus.subscribe(
        types.EventMessage, "foo", _handle
    )
    message_bus.publish(
        types.EventMessage(
            event_type="foo",
            payload="a"
        )
    )


def test_message_bus_query():
    dispatcher = MemoryDispatcher()
    dispatcher._topic = "query:foo"
    message_bus = MessageBus(dispatcher)
    message_bus.subscribe(
        types.QueryMessage, "foo", _handle
    )
    response_message = message_bus.query(
        types.QueryMessage(
            query_type="foo",
            payload="a",
            client_id="abc"
        )
    )
    assert response_message.payload == "b"

