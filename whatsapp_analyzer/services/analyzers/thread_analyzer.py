from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict
from .base_analyzer import BaseAnalyzer

class ThreadAnalyzer(BaseAnalyzer):
    """Analyzes conversation threads and their lengths."""

    THREAD_TIMEOUT_MINUTES = 30  # Messages more than 30 minutes apart are considered different threads

    @property
    def name(self) -> str:
        return "thread_analysis"

    def _parse_timestamp(self, timestamp: str) -> datetime:
        """Parse WhatsApp timestamp format."""
        try:
            # Try the format with AM/PM
            return datetime.strptime(timestamp.replace('\u202f', ' '), "%d/%m/%Y, %I:%M:%S %p")
        except ValueError:
            # Try 24-hour format if AM/PM format fails
            return datetime.strptime(timestamp.replace('\u202f', ' '), "%d/%m/%Y, %H:%M:%S")

    def analyze(self) -> Dict[str, Any]:
        threads = []
        current_thread = []
        last_message_time = None
        
        for msg in self.messages:
            current_time = self._parse_timestamp(msg.timestamp)
            
            # Check if this message belongs to the current thread
            if (last_message_time is None or 
                (current_time - last_message_time).total_seconds() / 60 <= self.THREAD_TIMEOUT_MINUTES):
                current_thread.append(msg)
            else:
                # Save the previous thread if it has more than one message
                if len(current_thread) > 1:
                    threads.append(current_thread)
                current_thread = [msg]
            
            last_message_time = current_time
        
        # Add the last thread if it exists
        if len(current_thread) > 1:
            threads.append(current_thread)
        
        # Analyze thread statistics
        thread_lengths = [len(thread) for thread in threads]
        longest_thread = max(threads, key=len) if threads else []
        
        return {
            "total_threads": len(threads),
            "average_thread_length": sum(thread_lengths) / len(thread_lengths) if thread_lengths else 0,
            "longest_thread_length": len(longest_thread),
            "longest_thread_preview": {
                "start_time": longest_thread[0].timestamp if longest_thread else None,
                "end_time": longest_thread[-1].timestamp if longest_thread else None,
                "participants": list(set(msg.sender for msg in longest_thread)) if longest_thread else []
            }
        } 