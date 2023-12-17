from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Load your trained machine learning model using Pickle
with open("spam_detection.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.route('/', methods=["POST"])
def classify_email():
    try:
        data = request.get_json()
        email_text = data.get('email')

        if email_text:
            # Perform feature extraction and classification using your model
            prediction = model.predict([email_text])[0]

            return jsonify({"classification": prediction})

        else:
            return jsonify({"error": "Invalid input."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
