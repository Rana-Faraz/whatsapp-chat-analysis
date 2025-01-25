import json
from typing import Dict

class ChatExporter:
    """Exporter for WhatsApp chat analysis results."""
    
    @staticmethod
    def export_to_json(data: Dict, file_path: str):
        """Export data to JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4) 