from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from services.verify_service import verify_entity
from services.research_service import generate_research
from utils.logger import get_logger

api = Blueprint('api', __name__)

# Logger
logger = get_logger()

# Limiter
limiter = Limiter(
    get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_response(success, data=None, error=None, status_code=200):
    """
    Creates a standardized JSON response for API endpoints.

    Args:
        success (bool): Indicates whether the operation was successful.
        data (dict or list, optional): The data payload to include in the response. Defaults to None.
        error (str or dict, optional): Error message or details if the operation failed. Defaults to None.
        status_code (int, optional): HTTP status code to return. Defaults to 200.

    Returns:
        tuple: A Flask Response object containing a JSON payload and the HTTP status code.
    """
    response = {
        "success": success,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response["data"] = data
    
    if error is not None:
        response["error"] = error
        
    return jsonify(response), status_code

@api.route('/verify', methods=['POST'])
@limiter.limit("10 per minute")
def verify():
    """
    POST endpoint to verify and identify an entity based on provided minimal information.

    Expects JSON payload with:
        - name (str): The name of the entity/person to verify.
        - affiliation (str): The affiliation or organization of the entity.
        - entityType (str, optional): Type of entity, either 'academic' or 'startup'. Defaults to 'academic'.

    Returns:
        Flask Response:
            - 200 OK if verification succeeds.
            - 400 Bad Request for missing/invalid input.
            - 422 Unprocessable Entity if verification fails with valid input.
            - 500 Internal Server Error for unexpected issues.
    """
    try:
        # Check if request contains JSON data
        if not request.is_json:
            logger.error("Request does not contain JSON data")
            return create_response(False, None, "Request must be JSON", 400)

        data = request.json

        # Validate required fields
        name = data.get('name', '').strip()
        affiliation = data.get('affiliation', '').strip()
        entity_type = data.get('entityType', 'academic')
        
        if not name:
            logger.error("Name is required and cannot be empty")
            return jsonify({"error": "Name is required and cannot be empty"}), 400
        
        if not affiliation:
            logger.error("Affiliation is required and cannot be empty")
            return jsonify({"error": "Affiliation is required and cannot be empty"}), 400
        
        if entity_type not in ["academic", "startup"]:
            logger.warning(f"Invalid entity_type: {entity_type}, defaulting to 'academic'")
            entity_type = "academic"
        
        # Process verification request
        result = verify_entity(
            name = name,
            affiliation = affiliation,
            entity_type = entity_type
        )
        
        # Check if verification was successful
        if result.get("verification_status") == "failed":
            if "error" in result and any(msg in result["error"].lower() for msg in ["invalid name", "invalid affiliation"]):
                return create_response(False, None, result, 400)
            return create_response(False, None, result, 422)
        
        return create_response(True, result, None, 200)

    except Exception as e:
        logger.error(f"Error running verification: {str(e)}")
        return create_response(False, None, "An unexpected error occurred", 500)

@api.route('/research', methods=['POST'])
@limiter.limit("10 per minute")
def research():
    """
    POST endpoint to generate comprehensive research output for a verified entity.

    Expects JSON payload with:
        - entityInfo (dict): Verified information about the entity.
        - entityType (str, optional): Type of entity, either 'academic' or 'startup'. Defaults to 'academic'.

    Returns:
        Flask Response:
            - 200 OK with generated research data.
            - 400 Bad Request if required data is missing.
            - 500 Internal Server Error for unexpected issues.
    """
    try:
        # Check if request contains JSON data
        if not request.is_json:
            logger.error("Request does not contain JSON data")
            return create_response(False, None, "Request must be JSON", 400)
        
        data = request.json

        # Validate required fields
        if not data.get('entityInfo'):
            logger.error(f"Error fetching entity info from request")
            return create_response(False, None, "Entity information is required", 400)
        
        # Process the research request
        result = generate_research(
            entity_info = data.get('entityInfo', {}),
            entity_type = data.get('entityType', 'academic')
        )

        return create_response(True, result, None, 200)
    
    except Exception as e:
        logger.error(f"Error running research: {str(e)}")
        return create_response(False, None, "An unexpected error occurred", 500)