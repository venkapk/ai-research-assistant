from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from utils.logger import get_logger
from databases import db
from databases.user import User
from routes.api import create_response

auth = Blueprint('auth', __name__)

# Logger
logger = get_logger()

@auth.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        # Check if request contains JSON data
        if not request.is_json:
            logger.error("Request does not contain JSON data")
            return create_response(False, None, "Request must be JSON", 400)
        
        data = request.json
        
        # Validate required fields
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()

        if not email:
            logger.error(f"User: {name}, Email is required")
            return create_response(False, None, "Email is required", 400)
        
        if not password or len(password) < 8:
            logger.error(f"User: {name}, Password is required and must be at least 8 characters")
            return create_response(False, None, "Password must be at least 8 characters", 400)
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            logger.error(f"User {name} already registered")
            return create_response(False, None, "User already registered", 409)
        
        # Create a new user
        new_user = User(email=email, password=password, name=name)

        # DB Session
        db.session.add(new_user)
        db.session.commit()

        # Generate JWT Token
        access_token = create_access_token(
            identity=str(new_user.id),
            expires_delta=timedelta(days=1)
        )

        return create_response(True, {
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "name": new_user.name
            },
            "token": access_token
        }, None, 201)

    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return create_response(False, None, "An error occurred during registration", 500)
    
@auth.route('/login', methods=['POST'])
def login():
    """Log in an existing user"""
    try:
        # Check if request contains JSON data
        if not request.is_json:
            logger.error("Request does not contain JSON data")
            return create_response(False, None, "Request must be JSON", 400)
        
        data = request.json
        
        # Validate required fields
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            logger.error(f"Email and password are required")
            return create_response(False, None, "Email and password are required", 400)
        
        # Find user
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            logger.error(f"Invalid email or password")
            return create_response(False, None, "Invalid email or password", 401)
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Generate JWT token
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(days=1)
        ) 

        return create_response(True, {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            },
            "token": access_token
        }, None, 200)

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return create_response(False, None, "An error occurred during login", 500)

@auth.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Get current user profile"""
    try:
        logger.info(f"JWT identity received: {get_jwt_identity()} (type: {type(get_jwt_identity()).__name__})")
        
        user_id = get_jwt_identity()

        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            logger.error(f"Invalid user_id format in token: {user_id}")
            return create_response(False, None, "Invalid authentication token", 401)

        user = User.query.get(user_id)
        
        if not user:
            logger.error(f"User not found")
            return create_response(False, None, "User not found", 404)
        
        return create_response(True, {
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
        }, None, 200)
        
    except Exception as e:
        logger.error(f"Profile retrieval error: {str(e)}")
        return create_response(False, None, "An error occurred retrieving profile", 500)