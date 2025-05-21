from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from databases import db, bcrypt
from databases.user import User
from databases.research_history import ResearchHistory

from routes.api import api
from routes.auth import auth
from routes.history import history
from utils.logger import get_logger
from datetime import datetime

# Logger
logger = get_logger()

# Initialize app
app = Flask(__name__)
CORS(app)

# Configure database
database_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'secret-key-change-me')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60 * 24  # 1 day
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(auth, url_prefix='/api/auth')
app.register_blueprint(history, url_prefix='/api/history')

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

@app.route('/api/health')
def health():
    """Health check route that also checks database connection"""
    try:
        # Test database connection
        db_status = "connected"
        try:
            db.session.execute('SELECT 1')
        except Exception as e:
            db_status = f"error: {str(e)}"
            
        return jsonify({
            "status": "online",
            "database": db_status,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting backend server at port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)