from dataclasses import dataclass

@dataclass
class Message:
    """Represents a WhatsApp message with timestamp, sender, and content."""
    timestamp: str
    sender: str
    message: str 