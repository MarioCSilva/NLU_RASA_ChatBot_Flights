import logging
from fastapi import WebSocket
from sqlalchemy.orm import Session
from typing import Dict, Tuple
from datetime import datetime
import aux.constants as Constants
from sql_app.crud import crud_user
class ConnectionManager:
    def __init__(self):
        # socket = (id, status)
        self.active_connections: Dict(int, Tuple(WebSocket, int, int)) = {}
        self.agent = None
    async def connect(self, websocket: WebSocket, client_id: int, db: Session):
        await websocket.accept()
        logging.info("New Connection Accepted")
        self.active_connections[client_id] = [
            websocket,
            Constants.NORMAL_STATUS,
            None]

    async def connect_agent(self, websocket: WebSocket, agent_id: int, client_id: int,db : Session):
        await websocket.accept()
        self.agent = agent_id
        agent_data = crud_user.get_userById(db,agent_id)
        
        self.active_connections[agent_id] = [
            websocket,
            Constants.REAl_AGENT_STATUS,
            client_id]
        self.update_receiver(client_id,agent_id)
        await self.send_message(
        client_id=client_id,
        msg_type=Constants.MESSAGE_TYPE_HELP_REQUEST_ACCEPTED,
        message=str(agent_data.username)
        )


    def get_users_requiring_help(self):
        return [user for user in self.active_connections 
         if self.active_connections[user][1] == Constants.HELP_REQUEST_STATUS]

    def disconnect(self, client_id: int):
        del self.active_connections[client_id]

    def should_talk_with_real_agent(self,client_id:int, msg_type:str):
        return self.active_connections[client_id][2] != None 
             #and msg_type != Constants.MESSAGE_TYPE_HELP_REQUEST_FINISHED

    def update_receiver(self,client_id:int, receiver_id):
        self.active_connections[client_id][2] = receiver_id

    def update_status(self, client_id, status):
        self.active_connections[client_id][1] = status

    async def  send_message(self, client_id: int, msg_type: str, message: str):
        data = {"content": message, "content_type": msg_type, "type":"receiver", "date": str(datetime.now())}
        logging.info(data)
        await self.active_connections[client_id][0].send_json({"topic": "receive", "data": data})

    async def broadcast(self, message: str):
        msg = {"content": message, "content_type": "feedback", "type":"receiver", "date":str(datetime.now())}
        for connection in self.active_connections:
            await self.active_connections[connection][0].send_json({"topic": "receive", "data": msg})

manager = ConnectionManager()