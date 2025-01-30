from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import tempfile
import os
from whatsapp_analyzer import ChatAnalysisService

app = Flask(__name__)

# Example heart emojis
heart_emojis = {
    '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❤️‍🔥', '❤️‍🩹', '♥️', '💗'
}

@app.route('/hello')
def hello():
    return "Hello, World!"

@app.route('/analyze', methods=['POST'])
def analyze_chat():
    """
    Endpoint to analyze a WhatsApp chat file.
    Accepts a chat file upload and returns the analysis results.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Create a temporary file to store the upload
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file.save(temp_file.name)
        temp_file_path = temp_file.name

    try:
        # Initialize and run the analysis service
        service = ChatAnalysisService(temp_file_path, heart_emojis)
        service.analyze()
        
        # Get the analysis results
        results = service.get_results()
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return jsonify(results)
    except Exception as e:
        # Clean up the temporary file in case of error
        os.unlink(temp_file_path)
        return jsonify({"error": f"Error analyzing chat file: {str(e)}"}), 500

@app.route('/')
def root():
    """Root endpoint that returns API information."""
    return jsonify({
        "message": "WhatsApp Chat Analyzer API",
        "usage": "POST /analyze with a chat file to analyze WhatsApp conversations"
    })

if __name__ == '__main__':
    app.run(debug=True) 