from datetime import datetime
from databases import db, bcrypt

class ResearchHistory(db.Model):
    __tablename__ = 'research_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    entity_name = db.Column(db.String(255), nullable=False)
    entity_affiliation = db.Column(db.String(255))
    entity_type = db.Column(db.String(50))
    research_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('research_history', lazy=True))