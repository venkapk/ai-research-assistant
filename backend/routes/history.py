from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from utils.logger import get_logger
from databases import db
from databases.research_history import ResearchHistory
from routes.api import create_response

history = Blueprint('history', __name__)

# Logger
logger = get_logger()

@history.route('/', methods=['GET'])
@jwt_required()
def get_history():
    """Get user's research history"""
    try:
        user_id = get_jwt_identity()

        # Get history items, most recent first
        history_items = ResearchHistory.query.filter_by(user_id=user_id).order_by(
            ResearchHistory.created_at.desc()
        ).all()

        # Format results
        results = []
        for item in history_items:
            results.append({
                "id": item.id,
                "entity_name": item.entity_name,
                "entity_affiliation": item.entity_affiliation,
                "entity_type": item.entity_type,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })

        return create_response(True, {"history": results}, None, 200)
    
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        return create_response(False, None, "An error occurred retrieving history", 500)
    
@history.route('/<int:history_id>', methods=['GET'])
@jwt_required()
def get_history_detail(history_id):
    """Get a specific research history item"""
    try:
        user_id = get_jwt_identity()
        
        # Get history item
        history_item = ResearchHistory.query.filter_by(
            id=history_id,
            user_id=user_id
        ).first()
        
        if not history_item:
            logger.error(f"History item not found")
            return create_response(False, None, "History item not found", 404)
        
        # Format result
        result = {
            "id": history_item.id,
            "entity_name": history_item.entity_name,
            "entity_affiliation": history_item.entity_affiliation,
            "entity_type": history_item.entity_type,
            "research_data": history_item.research_data,
            "created_at": history_item.created_at.isoformat() if history_item.created_at else None
        }
        
        return create_response(True, {"history_item": result}, None, 200)
        
    except Exception as e:
        logger.error(f"Error retrieving history detail: {str(e)}")
        return create_response(False, None, "An error occurred retrieving history detail", 500)

@history.route('/<int:history_id>', methods=['DELETE'])
@jwt_required()
def delete_history(history_id):
    """Delete a specific research history item"""
    try:
        user_id = get_jwt_identity()
        
        # Get history item
        history_item = ResearchHistory.query.filter_by(
            id=history_id,
            user_id=user_id
        ).first()
        
        if not history_item:
            logger.error(f"History item not found")
            return create_response(False, None, "History item not found", 404)
        
        # Delete the item
        db.session.delete(history_item)
        db.session.commit()
        
        return create_response(True, {"message": "History item deleted"}, None, 200)
        
    except Exception as e:
        logger.error(f"Error deleting history: {str(e)}")
        db.session.rollback()
        return create_response(False, None, "An error occurred deleting history", 500)