"""Main entry point for WhatsApp chat analysis."""

from whatsapp_analyzer import ChatAnalysisService

def main():
    # Example heart emojis
    heart_emojis = {
        '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❤️‍🔥', '❤️‍🩹', '♥️', '💗'
    }

    # Initialize and run the analysis service
    service = ChatAnalysisService('data/_chat.txt', heart_emojis)
    service.analyze()

if __name__ == "__main__":
    main() 