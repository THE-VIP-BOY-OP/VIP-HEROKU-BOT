import os
from asyncio import Queue as AsyncQueue
from asyncio import QueueEmpty
from typing import Any, Dict, Optional


class QueueManager:
    def __init__(self):
        self.queues: Dict[int, AsyncQueue] = {}

    async def add(self, chat_id: int, **params: Any):
        """Asynchronously add a set of parameters to the queue for a given chat_id."""
        if chat_id not in self.queues:
            self.queues[chat_id] = AsyncQueue()
        await self.queues[chat_id].put(params)

    async def get(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Asynchronously retrieve the first stored item for the given chat_id."""
        if chat_id in self.queues:
            try:
                return self.queues[chat_id].get_nowait()
            except QueueEmpty:
                return None
        return None

    async def remove(self, chat_id: int):
        """Asynchronously remove the first set of parameters for the given chat_id, and delete file if file_path exists."""
        if chat_id in self.queues:
            try:
                params = self.queues[chat_id].get_nowait()
                file_path = params.get("file_path")
                if file_path and os.path.exists(file_path):
                    os.remove(file_path)
                return params
            except QueueEmpty:
                raise ValueError(f"No parameters to remove for chat_id {chat_id}")
        else:
            raise ValueError(f"No queue found for chat_id {chat_id}")

    async def clear(self, chat_id: int):
        """Asynchronously clear the entire queue for a given chat_id, deleting files if file_path exists."""
        if chat_id in self.queues:
            while not self.queues[chat_id].empty():
                try:
                    params = self.queues[chat_id].get_nowait()
                    file_path = params.get("file_path")
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                except QueueEmpty:
                    break
            self.queues.pop(chat_id, None)

    async def has(self, chat_id: int) -> bool:
        """Check asynchronously if there is a queue for a given chat_id."""
        return chat_id in self.queues and not self.queues[chat_id].empty()


Queue = QueueManager()
