import re
from collections import Counter
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer

class WordAnalyzer(BaseAnalyzer):
    """Analyzer for word frequency and patterns."""

    @property
    def name(self) -> str:
        return "word_analysis"

    def analyze(self) -> Dict[str, Any]:
        return {
            "most_frequent_word": self._get_most_frequent_word(),
            "words_by_user": self._get_words_by_user(),
            "word_counts": self._get_word_counts()
        }

    def _get_most_frequent_word(self, min_length: int = 3):
        """Find the most frequently used word."""
        excluded_words = {'voice', 'call', 'missed', 'video', 'sticker', 'omitted'}
        word_counter = Counter()
        
        for msg in self.messages:
            words = re.findall(r'\b\w+\b', msg.message.lower())
            filtered_words = [w for w in words if len(w) >= min_length and w not in excluded_words]
            word_counter.update(filtered_words)
        
        if not word_counter:
            return {"message": "", "count": 0}
        
        word, count = word_counter.most_common(1)[0]
        return {"message": word, "count": count}

    def _get_words_by_user(self, min_length: int = 4):
        """Find most used words per user."""
        excluded_words = {'voice', 'call', 'missed', 'video', 'sticker', 'omitted'}
        user_word_counter = {}
        
        for msg in self.messages:
            if msg.sender not in user_word_counter:
                user_word_counter[msg.sender] = Counter()
            
            words = re.findall(r'\b\w+\b', msg.message.lower())
            filtered_words = [w for w in words if len(w) >= min_length and w not in excluded_words]
            user_word_counter[msg.sender].update(filtered_words)
        
        return {
            user: [
                {"word": word, "count": count}
                for word, count in counter.most_common(8)
            ]
            for user, counter in user_word_counter.items()
        }

    def _get_word_counts(self):
        """Count total words used by each user."""
        word_pattern = re.compile(r'\b\w+\b', re.UNICODE)
        user_word_counts = Counter()
        
        for msg in self.messages:
            words = word_pattern.findall(msg.message)
            user_word_counts[msg.sender] += len(words)
        
        return [
            {"name": user, "count": count}
            for user, count in user_word_counts.items()
        ] 