import re
from collections import Counter
from typing import Dict, Any, Set
from .base_analyzer import BaseAnalyzer

class EmojiAnalyzer(BaseAnalyzer):
    """Analyzer for emoji usage patterns."""

    def __init__(self, messages, heart_emojis: Set[str]):
        super().__init__(messages)
        self.heart_emojis = heart_emojis
        self._emoji_pattern = re.compile(
            u'[\U0001F600-\U0001F64F'
            u'\U0001F300-\U0001F5FF'
            u'\U0001F680-\U0001F6FF'
            u'\U0001F700-\U0001F77F'
            u'\U0001F780-\U0001F7FF'
            u'\U0001F800-\U0001F8FF'
            u'\U0001F900-\U0001F9FF'
            u'\U0001FA00-\U0001FA6F'
            u'\U0001FA70-\U0001FAFF'
            u'\U00002702-\U000027B0'
            u'\U000024C2-\U0001F251'
            u'\u2600-\u27BF'
            u'\u2300-\u23FF'
            u'\u2B50'
            u'\u2934-\u2935'
            u'\u2B06'
            u'\u2194-\u21AA'
            u'\u2934-\u2935'
            ']+', flags=re.UNICODE
        )

    @property
    def name(self) -> str:
        return "emoji_analysis"

    def analyze(self) -> Dict[str, Any]:
        return {
            "top_emojis": self._get_top_emojis(),
            "love_count": self._count_love()
        }

    def _extract_emojis(self, message: str):
        """Extract emojis from a message."""
        return self._emoji_pattern.findall(message)

    def _get_top_emojis(self, limit: int = 8):
        """Find most used emojis."""
        emoji_counter = Counter()
        
        for msg in self.messages:
            emojis = self._extract_emojis(msg.message)
            for emoji in emojis:
                for single_emoji in emoji:
                    if single_emoji in self.heart_emojis:
                        emoji_counter['❤️'] += 1
                    else:
                        emoji_counter[single_emoji] += 1
        
        return [
            {"emoji": emoji, "count": count}
            for emoji, count in emoji_counter.most_common(limit)
        ]

    def _count_love(self):
        """Count love expressions."""
        love_patterns = [
            r'\biloveyou\b',
            r'\blove\s+you\b',
            r'\blove\b'
        ]
        emoji_pattern = re.compile('|'.join(re.escape(emoji) for emoji in self.heart_emojis), re.UNICODE)
        count = 0
        
        for msg in self.messages:
            if any(re.search(pattern, msg.message, re.IGNORECASE) for pattern in love_patterns):
                count += 1
            if emoji_pattern.search(msg.message):
                count += 1
        
        return count 