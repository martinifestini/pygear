import asyncio
import pytest
from unittest.mock import MagicMock

from pygear.message_bus.middleware.scheduled import ScheduledMiddleware


@pytest.mark.asyncio
async def test_run():
    mock_message_bus = MagicMock()
    middleware = ScheduledMiddleware(mock_message_bus)
    middleware.schedule("bla", 1)
    await middleware.run()
    await asyncio.sleep(2)
    await middleware.stop()
    mock_message_bus.publish.assert_called_with("bla")
