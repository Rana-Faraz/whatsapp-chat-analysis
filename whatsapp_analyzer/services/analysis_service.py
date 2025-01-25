from typing import Set, Dict, Any
import json
from .parser import ChatParser
from .analyzers import AnalyzerRegistry

class ChatAnalysisService:
    """Service to orchestrate WhatsApp chat analysis."""

    def __init__(self, chat_file: str, heart_emojis: Set[str]):
        self.chat_file = chat_file
        self.heart_emojis = heart_emojis
        self.parser = ChatParser(chat_file)
        self.registry = AnalyzerRegistry()
        self.messages = None
        self.results = {}

    def analyze(self) -> Dict[str, Any]:
        """Perform chat analysis and return results."""
        self.messages = self.parser.parse()
        analyzers = self.registry.create_analyzers(self.messages, self.heart_emojis)
        
        # Run all analyzers and collect results
        for analyzer in analyzers:
            self.results[analyzer.name] = analyzer.analyze()
        
        # Export results to JSON
        self._export_results()
        self._print_results()
        return self.results
    
    def get_results(self):
        """Get analysis results."""
        return self.results

    def _export_results(self):
        """Export analysis results to JSON file."""
        with open('data/chat_analysis_results.json', 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)

    def _print_results(self):
        """Print analysis results."""
        word_results = self.results.get("word_analysis", {})
        time_results = self.results.get("time_analysis", {})
        emoji_results = self.results.get("emoji_analysis", {})
        sentiment_results = self.results.get("sentiment_analysis", {})

        # Print word analysis results
        most_frequent = word_results.get("most_frequent_word", {})
        print(f"\nMost frequent word: '{most_frequent.get('message', '')}' "
              f"with count: {most_frequent.get('count', 0)}")

        # Print time analysis results
        print("\nMessages count by day of the week:")
        for day_data in time_results.get("messages_per_day", []):
            print(f"{day_data['day']}: {day_data['count']}")

        # Print user message counts
        time_data = time_results.get("messages_by_time", [])
        for user_data in time_data:
            print(f"\nUser: {user_data['name']}")
            print(f"Morning: {user_data['morning']}")
            print(f"Night: {user_data['night']}")

        # Print emoji analysis results
        print("\nTop 8 most used emojis:")
        for emoji_data in emoji_results.get("top_emojis", []):
            print(f"{emoji_data['emoji']}: {emoji_data['count']}")

        # Print word usage by user
        print("\nTop 8 words used by each user:")
        for user, words in word_results.get("words_by_user", {}).items():
            print(f"\nUser: {user}")
            for word_data in words:
                print(f"{word_data['word']}: {word_data['count']}")

        # Print time spent
        print("\nTime spent messaging by each user (in days):")
        for time_data in time_results.get("time_spent", []):
            print(f"{time_data['name']}: {time_data['days']:.2f} days")

        # Print call duration
        print(f"\nTotal time spent on calls: {time_results.get('call_duration', 0):.2f} hours")

        # Print sentiment analysis results
        print(f"Total count of laughter occurrences: {sentiment_results.get('laughter_count', 0)}")
        print(f"Total count of love occurrences: {emoji_results.get('love_count', 0)}")

        # Print word counts
        print("\nTotal words by user:")
        for word_count in word_results.get("word_counts", []):
            print(f"{word_count['name']}: {word_count['count']} words") 