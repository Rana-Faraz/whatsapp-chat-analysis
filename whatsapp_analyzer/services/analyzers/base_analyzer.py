from abc import ABC, abstractmethod
from typing import Any, Dict, List
from ...models.message import Message

class BaseAnalyzer(ABC):
    """Base interface for all chat analyzers."""
    
    def __init__(self, messages: List[Message]):
        self.messages = messages
        
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Perform analysis and return results."""
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the analyzer."""
        pass 