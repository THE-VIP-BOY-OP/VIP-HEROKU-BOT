import asyncio
from typing import Any, Dict, Optional


class QueueManager:
    def __init__(self):
        self.queues: Dict[int, asyncio.Queue] = {}

    async def add_queue(self, chat_id: int, **params: Any):
        """Asynchronously add a set of parameters to the queue for a given chat_id."""
        if chat_id not in self.queues:
            self.queues[chat_id] = asyncio.Queue()
        await self.queues[chat_id].put(params)

    async def retrieve(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Asynchronously retrieve the first stored item for the given chat_id."""
        if chat_id in self.queues:
            try:
                return self.queues[chat_id].get_nowait()
            except asyncio.QueueEmpty:
                return None
        return None

    async def remove(self, chat_id: int):
        """Asynchronously remove the first set of parameters for the given chat_id."""
        if chat_id in self.queues:
            try:
                await self.queues[chat_id].get_nowait()
            except asyncio.QueueEmpty:
                raise ValueError(f"No parameters to remove for chat_id {chat_id}")
        else:
            raise ValueError(f"No queue found for chat_id {chat_id}")

    async def clear_queue(self, chat_id: int):
        """Asynchronously clear the entire queue for a given chat_id."""
        if chat_id in self.queues:
            self.queues.pop(chat_id, None)

    async def has_queue(self, chat_id: int) -> bool:
        """Check asynchronously if there is a queue for a given chat_id."""
        return chat_id in self.queues and not self.queues[chat_id].empty()
