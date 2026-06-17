from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    provider: str = "base"

    @abstractmethod
    async def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
