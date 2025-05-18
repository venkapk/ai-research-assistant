from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from routes.api import api
from utils.logger import get_logger
import os

# Logger
logger = get_logger()

# Initialize app
app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    try:
        logger.info("Health check route '/' called.")
        return jsonify({
        "status": "online",
        "name": "AI Research Tool API",
        "description": "AI-powered research assistant for academic professionals and startup founders",
        "version": "1.0.0"
        })
    except Exception as e:
            logger.error(f"Error running application: {str(e)}")
            return jsonify({"message": "Error running API"}), 500
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting backend server at port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)