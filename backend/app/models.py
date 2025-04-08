from datetime import datetime
from . import db

class Vulnerability(db.Model):
    __tablename__ = 'vulnerabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    defender_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20))
    discovered_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationship: one vulnerability can have many reviews.
    reviews = db.relationship('Review', backref='vulnerability', lazy=True)

    def __repr__(self):
        return f'<Vulnerability {self.defender_id} - {self.title}>'

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    vulnerability_id = db.Column(db.Integer, db.ForeignKey('vulnerabilities.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # e.g., pending, in_review, remediated
    comments = db.Column(db.Text)
    reviewed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Review for Vulnerability {self.vulnerability_id} - {self.status}>'

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    ticket_number = db.Column(db.String(50), unique=True)
    status = db.Column(db.String(50), default='open')  # open, closed, in_progress, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ticket {self.ticket_number} for Review {self.review_id}>'
