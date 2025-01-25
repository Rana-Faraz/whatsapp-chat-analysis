import re
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer

class SentimentAnalyzer(BaseAnalyzer):
    """Analyzer for sentiment and emotional expressions."""

    @property
    def name(self) -> str:
        return "sentiment_analysis"

    def analyze(self) -> Dict[str, Any]:
        return {
            "laughter_count": self._count_laughter()
        }

    def _count_laughter(self):
        """Count laughter occurrences."""
        laughter_patterns = [
            r'\b(h+a+)+\b',
            r'\b(l+o+)+l+\b',
            r'\b(l+m+a+o+)+\b',
            r'\b(l+m+f+a+o+)+\b'
        ]
        emoji_pattern = re.compile(r'😂|🤣', re.UNICODE)
        count = 0
        
        for msg in self.messages:
            if any(re.search(pattern, msg.message, re.IGNORECASE) for pattern in laughter_patterns):
                count += 1
            if emoji_pattern.search(msg.message):
                count += 1
        
        return count 