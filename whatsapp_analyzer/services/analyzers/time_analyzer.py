import re
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer

class TimeAnalyzer(BaseAnalyzer):
    """Analyzer for time-based patterns."""

    @property
    def name(self) -> str:
        return "time_analysis"

    def analyze(self) -> Dict[str, Any]:
        return {
            "messages_per_day": self._get_messages_per_day(),
            "messages_by_time": self._get_messages_by_time(),
            "time_spent": self._get_time_spent(),
            "call_duration": self._get_call_duration()
        }

    def _get_messages_per_day(self):
        """Count messages per day of the week."""
        day_counter = Counter()
        date_formats = [
            '%m/%d/%y, %I:%M:%S %p',  # US format: MM/DD/YY
            '%d/%m/%y, %I:%M:%S %p',  # International format: DD/MM/YY
            '%m/%d/%Y, %I:%M:%S %p',  # US format with 4-digit year
            '%d/%m/%Y, %I:%M:%S %p',  # International format with 4-digit year
        ]
        
        for msg in self.messages:
            parsed = False
            for date_format in date_formats:
                try:
                    dt = datetime.strptime(msg.timestamp, date_format)
                    day_of_week = dt.strftime('%A')
                    day_counter[day_of_week] += 1
                    parsed = True
                    break
                except ValueError:
                    continue
        
        return [
            {"day": day, "count": count}
            for day, count in day_counter.items()
        ]

    def _get_messages_by_time(self):
        """Count messages by time of day per user."""
        user_time_counts = defaultdict(lambda: {'morning': 0, 'night': 0})
        
        for msg in self.messages:
            time_str = msg.timestamp.split(',')[1].strip()
            hour = int(time_str.split(':')[0])
            period = 'morning' if 6 <= hour < 18 else 'night'
            user_time_counts[msg.sender][period] += 1
        
        return [
            {
                "name": user,
                "morning": counts['morning'],
                "night": counts['night']
            }
            for user, counts in user_time_counts.items()
        ]

    def _get_time_spent(self):
        """Calculate time spent messaging by user."""
        user_message_count = Counter(msg.sender for msg in self.messages)
        return [
            {"name": user, "days": count / (60 * 24)}
            for user, count in user_message_count.items()
        ]

    def _get_call_duration(self):
        """Calculate total time spent on calls."""
        total_seconds = 0
        
        for msg in self.messages:
            if 'call' in msg.message.lower():
                if duration_match := re.search(r'(?:Video call|Voice call),\s*(.*)', msg.message, re.IGNORECASE):
                    duration = duration_match.group(1)
                    total_seconds += self._duration_to_seconds(duration)
        
        return total_seconds / 3600

    def _duration_to_seconds(self, duration: str) -> int:
        """Convert duration string to seconds."""
        patterns = {
            'hr': r'(\d+)\s*hr',
            'min': r'(\d+)\s*min',
            'sec': r'(\d+)\s*sec'
        }
        
        total_seconds = 0
        for unit, pattern in patterns.items():
            if match := re.search(pattern, duration):
                value = int(match.group(1))
                if unit == 'hr':
                    total_seconds += value * 3600
                elif unit == 'min':
                    total_seconds += value * 60
                else:
                    total_seconds += value
        
        return total_seconds 