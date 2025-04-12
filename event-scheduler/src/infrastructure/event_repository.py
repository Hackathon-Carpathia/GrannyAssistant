from datetime import date
from typing import List, Optional
from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.types import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from src.domain.event import RegisterEvent, Event
from src.infrastructure.sql_connector import DatabaseConnector, Base
from datetime import datetime



class RegisterEventModel(Base):
    __tablename__ = 'registered_event'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    prompt = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    hours = Column(JSON, nullable=False)

    @classmethod
    def of(cls, event: RegisterEvent) -> "RegisterEventModel":
        return cls(
            user_id=event.user_id,
            prompt=event.prompt,
            start_date=event.start_date,
            end_date=event.end_date,
            hours=event.hours,
        )

    def to_event(self) -> Event:
        return Event(
            user_id=self.user_id,
            prompt=self.prompt
        )
    
@dataclass
class RegisterEventRepository:
    connector: DatabaseConnector

    def create(self, event: RegisterEvent):
        session = self.connector.get_session()
        model = RegisterEventModel.of(event)
        session.add(model)
        session.commit()


    def read_events_to_execute(self) -> List[RegisterEvent]:
        session = self.connector.get_session()
        now = datetime.now()
        today = now.date()
        current_hour = now.hour

        models = session.query(RegisterEventModel).all()
        # models = session.query(RegisterEventModel).filter(
        #     RegisterEventModel.start_date <= today,
        #     RegisterEventModel.end_date >= today
        # ).all()

        filtered = [
            model.to_event()
            for model in models
            # if current_hour in model.hours
        ]

        print(filtered)

        return filtered
