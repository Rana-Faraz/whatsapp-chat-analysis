import re
from typing import List
from ..models.message import Message

class ChatParser:
    """Parser for WhatsApp chat export files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._pattern = re.compile(r'\[(.*?)\] (.*?): (.*)')

    def parse(self) -> List[Message]:
        """Parse WhatsApp chat file and return list of Message objects."""
        messages = []
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            next(file)  # Skip first line
            for line in file:
                if match := self._pattern.match(line):
                    timestamp, sender, message = match.groups()
                    # Skip system messages about phone number changes
                    if "changed their phone number" not in message:
                        messages.append(Message(timestamp, sender, message))
        
        return messages 