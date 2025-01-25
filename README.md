# WhatsApp Chat Analyzer

A Python package for analyzing WhatsApp chat export files. This tool provides detailed insights into your WhatsApp conversations, including message patterns, emoji usage, and more.

## Features

- Message frequency analysis by user and day
- Emoji usage statistics
- Word frequency analysis
- Time-based message pattern analysis
- Call duration tracking
- Sentiment analysis (laughter and love expressions)
- Detailed JSON export of analysis results

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/whatsapp-chat-analysis.git
cd whatsapp-chat-analysis
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Export your WhatsApp chat:

   - Open the WhatsApp chat
   - Click on the three dots (⋮)
   - Select "More"
   - Choose "Export chat"
   - Save the exported file as "data/\_chat.txt" in the project directory

2. Run the analysis:

```bash
python main.py
```

The analysis results will be:

- Printed to the console
- Exported to `chat_analysis_results.json`

## Project Structure

```
whatsapp_analyzer/
├── models/
│   ├── __init__.py
│   └── message.py
├── services/
│   ├── __init__.py
│   ├── analysis_service.py
│   ├── parser.py
│   └── analyzers/
│       ├── __init__.py
│       ├── base_analyzer.py
│       ├── analyzer_registry.py
│       ├── word_analyzer.py
│       ├── emoji_analyzer.py
│       ├── time_analyzer.py
│       └── sentiment_analyzer.py
└── __init__.py
```

## Adding New Analyzers

The project uses a modular architecture that makes it easy to add new types of analysis. Here's how to create a new analyzer:

1. Create a new file in `whatsapp_analyzer/services/analyzers/` (e.g., `my_analyzer.py`):

```python
from typing import Dict, Any
from .base_analyzer import BaseAnalyzer

class MyAnalyzer(BaseAnalyzer):
    """Description of what your analyzer does."""

    @property
    def name(self) -> str:
        return "my_analysis"  # This will be the key in results dictionary

    def analyze(self) -> Dict[str, Any]:
        # Implement your analysis logic here
        return {
            "result_key": self._analyze_something(),
            "another_result": self._analyze_something_else()
        }

    def _analyze_something(self):
        # Helper method for your analysis
        result = 0
        for msg in self.messages:  # self.messages is available from BaseAnalyzer
            # Your analysis logic here
            pass
        return result
```

2. Register your analyzer in `analyzer_registry.py`:

```python
from .my_analyzer import MyAnalyzer

class AnalyzerRegistry:
    def _register_default_analyzers(self):
        # ... existing registrations ...
        self.register_analyzer("my_analyzer", MyAnalyzer)
```

3. Export your analyzer in `analyzers/__init__.py`:

```python
from .my_analyzer import MyAnalyzer

__all__ = [
    # ... existing exports ...
    'MyAnalyzer'
]
```

4. Access results in `analysis_service.py`:

```python
def _print_results(self):
    # ... existing code ...
    my_results = self.results.get("my_analysis", {})
    print(f"\nMy analysis results:")
    print(f"Something: {my_results.get('result_key')}")
```

### Tips for Creating Analyzers

1. **Naming Convention**: Use descriptive names for your analyzer class and methods
2. **Documentation**: Add docstrings to explain what your analyzer does
3. **Type Hints**: Use proper type hints for better code maintainability
4. **Error Handling**: Handle potential errors gracefully
5. **Results Format**: Return results in a dictionary with clear, descriptive keys
6. **Message Access**: Use `self.messages` to access the list of chat messages
7. **Helper Methods**: Break down complex analysis into private helper methods

## Analysis Output

The tool provides the following insights:

1. Message Statistics:

   - Most frequent words
   - Messages per day
   - Messages per user
   - Morning vs. night message patterns

2. Emoji Analysis:

   - Top emojis used
   - Heart emoji usage

3. User Behavior:

   - First message by each user
   - Time spent messaging
   - Word count per user

4. Call Analysis:

   - Total call duration

5. Sentiment Indicators:
   - Laughter occurrences
   - Love expressions

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
