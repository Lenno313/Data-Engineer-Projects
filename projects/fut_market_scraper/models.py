from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Player(Base):
    __tablename__ = 'players'
    
    futwiz_id = Column(Integer, primary_key=True, autoincrement=False)
    
    first_name = Column(String)
    last_name = Column(String)
    
    # Weitere Daten (Erweiterbar)
    rating = Column(Integer)
    main_position = Column(String)
    skill_moves = Column(Integer)
    weak_foot = Column(Integer)
    
    # Verknüpfung zu den Preisen
    prices = relationship("Price", back_populates="player")

class Price(Base):
    __tablename__ = 'prices'
    
    id = Column(Integer, primary_key=True)

    player_id = Column(Integer, ForeignKey('players.futwiz_id'))

    price_value = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    player = relationship("Player", back_populates="prices")

class RatingSnapshot(Base):
    __tablename__ = 'rating_snapshots'
    
    id = Column(Integer, primary_key=True)

    rating = Column(Integer, nullable=False)   # 84, 85...
    rank = Column(Integer)                     # 1, 2, 3... (für die Top X dieses Ratings)
    
    price_value = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow) # Top-X identifizierbar anhand dieses Zeitstempels
