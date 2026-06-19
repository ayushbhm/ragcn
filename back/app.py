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
app.debug = True
if __name__ == '__main__': 
 app.run(port=5000)
