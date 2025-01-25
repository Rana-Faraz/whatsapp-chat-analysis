from datetime import datetime
from typing import Dict, Any
from collections import defaultdict
from .base_analyzer import BaseAnalyzer

class ConversationStarterAnalyzer(BaseAnalyzer):
    """Analyzes which users tend to start new conversations."""

    CONVERSATION_GAP_MINUTES = 360  # 6 hours gap defines a new conversation

    @property
    def name(self) -> str:
        return "conversation_starter_analysis"

    def _parse_timestamp(self, timestamp: str) -> datetime:
        """Parse WhatsApp timestamp format."""
        try:
            # Try the format with AM/PM
            return datetime.strptime(timestamp.replace('\u202f', ' '), "%d/%m/%Y, %I:%M:%S %p")
        except ValueError:
            # Try 24-hour format if AM/PM format fails
            return datetime.strptime(timestamp.replace('\u202f', ' '), "%d/%m/%Y, %H:%M:%S")

    def analyze(self) -> Dict[str, Any]:
        conversation_starters = defaultdict(int)
        last_message_time = None
        
        for msg in self.messages:
            current_time = self._parse_timestamp(msg.timestamp)
            
            # If there's no last message or the gap is large enough, this is a new conversation
            if (last_message_time is None or 
                (current_time - last_message_time).total_seconds() / 60 > self.CONVERSATION_GAP_MINUTES):
                conversation_starters[msg.sender] += 1
            
            last_message_time = current_time
        
        # Calculate percentages
        total_conversations = sum(conversation_starters.values())
        starter_percentages = {
            user: (count / total_conversations * 100) if total_conversations > 0 else 0
            for user, count in conversation_starters.items()
        }
        
        return {
            "conversation_starters_count": dict(conversation_starters),
            "starter_percentages": starter_percentages,
            "top_starter": max(conversation_starters.items(), key=lambda x: x[1]) if conversation_starters else None
        } 