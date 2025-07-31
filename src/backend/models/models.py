"""
Database models for multi-user support
"""

from sqlalchemy import Column, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

Base = declarative_base()

class User(Base):
    """User model for session management"""
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True)
    spotify_token = Column(Text, nullable=True)
    spotify_refresh_token = Column(Text, nullable=True)
    spotify_token_expires = Column(DateTime, nullable=True)
    youtube_token = Column(Text, nullable=True)
    youtube_refresh_token = Column(Text, nullable=True)
    youtube_token_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DatabaseManager:
    """Database manager for user sessions"""
    
    def __init__(self, database_url="sqlite:///users.db"):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def get_or_create_user(self, user_id: str) -> User:
        """Get existing user or create new one"""
        user = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id)
            self.session.add(user)
            self.session.commit()
        return user
    
    def update_spotify_tokens(self, user_id: str, access_token: str, refresh_token: str, expires_in: int):
        """Update Spotify tokens for user"""
        user = self.get_or_create_user(user_id)
        user.spotify_token = access_token
        user.spotify_refresh_token = refresh_token
        user.spotify_token_expires = datetime.utcnow().replace(second=datetime.utcnow().second + expires_in)
        self.session.commit()
    
    def update_youtube_tokens(self, user_id: str, credentials_dict: dict):
        """Update YouTube tokens for user"""
        user = self.get_or_create_user(user_id)
        user.youtube_token = json.dumps(credentials_dict)
        self.session.commit()
    
    def get_spotify_tokens(self, user_id: str) -> dict:
        """Get Spotify tokens for user"""
        user = self.get_or_create_user(user_id)
        if user.spotify_token and user.spotify_token_expires > datetime.utcnow():
            return {
                "access_token": user.spotify_token,
                "refresh_token": user.spotify_refresh_token,
                "expires_at": user.spotify_token_expires
            }
        return None
    
    def get_youtube_tokens(self, user_id: str) -> dict:
        """Get YouTube tokens for user"""
        user = self.get_or_create_user(user_id)
        if user.youtube_token:
            return json.loads(user.youtube_token)
        return None
    
    def is_spotify_authenticated(self, user_id: str) -> bool:
        """Check if user has valid Spotify tokens"""
        tokens = self.get_spotify_tokens(user_id)
        return tokens is not None and tokens["expires_at"] > datetime.utcnow()
    
    def is_youtube_authenticated(self, user_id: str) -> bool:
        """Check if user has valid YouTube tokens"""
        tokens = self.get_youtube_tokens(user_id)
        return tokens is not None 