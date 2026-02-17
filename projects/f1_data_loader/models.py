from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

class F1Race(Base):
    __tablename__ = "f1_races"
    id = Column(Integer, primary_key=True)
    season = Column(Integer)
    round = Column(Integer)
    circuit_name = Column(String)
    date = Column(String)

class F1Result(Base):
    __tablename__ = "f1_results"
    id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey("f1_races.id"))
    driver_name = Column(String)
    constructor = Column(String)
    position = Column(Integer)
    points = Column(Float)
    fastest_lap_time = Column(String)
