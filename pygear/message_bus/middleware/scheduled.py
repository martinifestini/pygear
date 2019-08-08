import asyncio
import typing


class Middleware:
    def __init__(self, message_bus):
        self.message_bus = message_bus


class ScheduledMiddleware(Middleware):
    _tasks: typing.List[asyncio.Task]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scheduled_tasks = list()
        self._tasks = list()

    def schedule(self, msg, delay):
        async def func():
            await asyncio.sleep(delay)
            self.message_bus.publish(msg)
        self._scheduled_tasks.append(
            func
        )
    
    def _create_tasks(self):
        for func in self._scheduled_tasks:
            self._tasks.append(
                asyncio.create_task(func())
            )

    async def run(self):
        self._create_tasks()
    
    async def stop(self):
        for task in self._tasks:
            task.cancel()
        
        return await asyncio.gather(*self._tasks)