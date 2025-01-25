from typing import Dict, List, Type, Set
from ...models.message import Message
from .base_analyzer import BaseAnalyzer
from .word_analyzer import WordAnalyzer
from .emoji_analyzer import EmojiAnalyzer
from .time_analyzer import TimeAnalyzer
from .sentiment_analyzer import SentimentAnalyzer

class AnalyzerRegistry:
    """Registry for managing and creating analyzers."""

    def __init__(self):
        self._analyzers: Dict[str, Type[BaseAnalyzer]] = {}
        self._register_default_analyzers()

    def _register_default_analyzers(self):
        """Register the default set of analyzers."""
        self.register_analyzer("word", WordAnalyzer)
        self.register_analyzer("emoji", EmojiAnalyzer)
        self.register_analyzer("time", TimeAnalyzer)
        self.register_analyzer("sentiment", SentimentAnalyzer)

    def register_analyzer(self, name: str, analyzer_class: Type[BaseAnalyzer]):
        """Register a new analyzer."""
        self._analyzers[name] = analyzer_class

    def create_analyzers(self, messages: List[Message], heart_emojis: Set[str] = None) -> List[BaseAnalyzer]:
        """Create instances of all registered analyzers."""
        instances = []
        for name, analyzer_class in self._analyzers.items():
            if name == "emoji" and heart_emojis is not None:
                instances.append(analyzer_class(messages, heart_emojis))
            else:
                instances.append(analyzer_class(messages))
        return instances

    def get_available_analyzers(self) -> List[str]:
        """Get list of registered analyzer names."""
        return list(self._analyzers.keys()) 