from datetime import datetime
from typing import Dict, Any
from collections import defaultdict
from .base_analyzer import BaseAnalyzer

class ResponseTimeAnalyzer(BaseAnalyzer):
    """Analyzes response times between users in the chat."""

    @property
    def name(self) -> str:
        return "response_time_analysis"

    def _parse_timestamp(self, timestamp: str) -> datetime:
        """Parse WhatsApp timestamp format."""
        try:
            # Try the format with AM/PM
            return datetime.strptime(timestamp.replace('\u202f', ' '), "%d/%m/%Y, %I:%M:%S %p")
        except ValueError:
            # Try 24-hour format if AM/PM format fails
            return datetime.strptime(timestamp.replace('\u202f', ' '), "%d/%m/%Y, %H:%M:%S")

    def analyze(self) -> Dict[str, Any]:
        response_times = defaultdict(list)
        user_last_message = {}
        
        for msg in self.messages:
            current_time = self._parse_timestamp(msg.timestamp)
            current_sender = msg.sender
            
            # Check for responses to other users
            for other_user, last_msg_time in user_last_message.items():
                if other_user != current_sender:
                    time_diff = (current_time - last_msg_time).total_seconds() / 60  # in minutes
                    # Only count responses within 12 hours to avoid counting new conversation starts
                    if time_diff <= 720:  # 12 hours in minutes
                        response_times[f"{other_user}->{current_sender}"].append(time_diff)
            
            user_last_message[current_sender] = current_time
        
        # Calculate average response times
        avg_response_times = {}
        for user_pair, times in response_times.items():
            if times:
                avg_response_times[user_pair] = sum(times) / len(times)
        
        return {
            "average_response_times": avg_response_times,
            "fastest_responder": min(avg_response_times.items(), key=lambda x: x[1]) if avg_response_times else None,
            "slowest_responder": max(avg_response_times.items(), key=lambda x: x[1]) if avg_response_times else None
        } 