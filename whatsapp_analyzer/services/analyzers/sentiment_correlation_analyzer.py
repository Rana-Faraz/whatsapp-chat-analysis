from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict
import re
from .base_analyzer import BaseAnalyzer

class SentimentCorrelationAnalyzer(BaseAnalyzer):
    """Analyzes how users' sentiments correlate during interactions."""

    INTERACTION_WINDOW_MINUTES = 10  # Consider messages within 10 minutes as related
    
    # Simple sentiment indicators (can be expanded)
    POSITIVE_PATTERNS = [
        r'😊|😄|😃|❤️|💕|👍|♥️|😍|🥰',  # positive emojis
        r'\b(?:haha|lol|lmao|xd|love|thanks|great|awesome|nice)\b',  # positive words
    ]
    
    NEGATIVE_PATTERNS = [
        r'😢|😭|😠|😡|👎|😕|😞|😔',  # negative emojis
        r'\b(?:sad|angry|upset|sorry|bad|hate|terrible|awful)\b',  # negative words
    ]

    @property
    def name(self) -> str:
        return "sentiment_correlation_analysis"

    def _parse_timestamp(self, timestamp: str) -> datetime:
        """Parse WhatsApp timestamp format."""
        try:
            # Try the format with AM/PM
            return datetime.strptime(timestamp.replace('\u202f', ' '), "%d/%m/%Y, %I:%M:%S %p")
        except ValueError:
            # Try 24-hour format if AM/PM format fails
            return datetime.strptime(timestamp.replace('\u202f', ' '), "%d/%m/%Y, %H:%M:%S")

    def _get_message_sentiment(self, message: str) -> float:
        """Calculate a simple sentiment score for a message."""
        message = message.lower()
        
        positive_count = sum(len(re.findall(pattern, message)) 
                           for pattern in self.POSITIVE_PATTERNS)
        negative_count = sum(len(re.findall(pattern, message)) 
                           for pattern in self.NEGATIVE_PATTERNS)
        
        if positive_count == 0 and negative_count == 0:
            return 0
        return (positive_count - negative_count) / (positive_count + negative_count)

    def analyze(self) -> Dict[str, Any]:
        user_interactions = defaultdict(list)
        sentiment_correlations = defaultdict(list)
        
        # Group messages by time windows and calculate sentiments
        current_window = []
        last_time = None
        
        for msg in self.messages:
            current_time = self._parse_timestamp(msg.timestamp)
            
            if (last_time is None or 
                (current_time - last_time).total_seconds() / 60 <= self.INTERACTION_WINDOW_MINUTES):
                current_window.append((msg, self._get_message_sentiment(msg.message)))
            else:
                # Analyze sentiment correlations in the current window
                if len(current_window) > 1:
                    for i, (msg1, sent1) in enumerate(current_window[:-1]):
                        for msg2, sent2 in current_window[i+1:]:
                            if msg1.sender != msg2.sender:
                                pair_key = tuple(sorted([msg1.sender, msg2.sender]))
                                sentiment_correlations[pair_key].append((sent1, sent2))
                
                current_window = [(msg, self._get_message_sentiment(msg.message))]
            
            last_time = current_time
        
        # Calculate final correlations
        correlations = {}
        for pair, sentiments in sentiment_correlations.items():
            if len(sentiments) > 1:  # Need at least 2 interactions
                # Calculate how often sentiments match (both positive, both negative, or both neutral)
                matching_sentiments = sum(1 for s1, s2 in sentiments 
                                       if (s1 > 0 and s2 > 0) or 
                                          (s1 < 0 and s2 < 0) or 
                                          (s1 == 0 and s2 == 0))
                correlation = matching_sentiments / len(sentiments)
                correlations[f"{pair[0]}<->{pair[1]}"] = correlation
        
        # Find users who influence others' sentiments
        sentiment_influencers = defaultdict(float)
        for pair, sentiments in sentiment_correlations.items():
            if len(sentiments) > 1:
                # Check how often the second user's sentiment matches the first user's previous sentiment
                for i in range(len(sentiments)-1):
                    if sentiments[i][0] != 0 and sentiments[i+1][1] != 0:
                        if (sentiments[i][0] > 0 and sentiments[i+1][1] > 0) or \
                           (sentiments[i][0] < 0 and sentiments[i+1][1] < 0):
                            sentiment_influencers[pair[0]] += 1
        
        return {
            "sentiment_correlations": correlations,
            "top_correlated_pairs": sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:3],
            "sentiment_influencers": dict(sentiment_influencers),
            "total_analyzed_interactions": sum(len(sents) for sents in sentiment_correlations.values())
        } 