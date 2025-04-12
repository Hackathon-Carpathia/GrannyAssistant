from src.infrastructure.event_repository import RegisterEventRepository
from src.infrastructure.sql_connector import DatabaseConnector
import os
from fastapi import Depends
from src.infrastructure.event_service import EventService

dependencies = {}

def initialize_dependecies():
    global dependencies

    _event_repository = RegisterEventRepository(connector=DatabaseConnector())

    _event_service = EventService(event_repository=_event_repository)


    dependencies[EventService] = _event_service
    dependencies[RegisterEventRepository] = _event_repository
        

def get_event_service():
    return dependencies[EventService]

def get_event_repository():
    return dependencies[RegisterEventRepository]