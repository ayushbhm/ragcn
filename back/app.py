import os
from flask import Flask
from routes.main import main

from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(main)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.config['SESSIONS'] = {}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)