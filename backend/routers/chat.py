import logging
from fastapi import WebSocket, APIRouter, Depends, WebSocketDisconnect
from sql_app.crud import crud_message, crud_feedback
from sql_app.schemas import messages, feedback
from sqlalchemy.orm import Session
import aux.utils as Utils
from bot.chatbot import chatbotclient
from bot.connection_manager import manager
import  logging
import aux.constants as Constants
# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)

router = APIRouter()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, db:Session = Depends(Utils.get_db)):

    await manager.connect(websocket, client_id, db=db)
    #await chatbotclient.send(db, client_id, {"content": "hello", "content_type": Constants.MESSAGE_TYPE_TEXT})
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            content_type = data["content_type"]
            data = data["content"]
            msg_data = messages.MessageCreate(
                sender=client_id,
                receiver=manager.active_connections[client_id][2],
                content=data,
                content_type=content_type
            )

            # If  talking directly to the a real agent
            if manager.should_talk_with_real_agent(client_id, content_type):
                await manager.send_message(
                    manager.active_connections[client_id][2],
                    content_type,
                    data,
                    )
            else:
                # Else, talking to the bot..
                await chatbotclient.send(db,client_id, {"content":data, "content_type": content_type})
                crud_message.create(msg_data, db=db)
           
           
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        # await manager.broadcast(f"Client #{client_id} left the chat")

@router.websocket("/ws/agent/{agent_id}/client/{client_id}")
async def websocket_endpoint(websocket: WebSocket, agent_id: int,client_id:int, db:Session = Depends(Utils.get_db)):
    await manager.connect_agent(websocket, agent_id, client_id,db)
    try:
        while True:
            data = await websocket.receive_json()
            content_type = data["content_type"]
            data = data["content"]
            msg_data = messages.MessageCreate(
                sender=client_id,
                receiver=manager.active_connections[client_id][2],
                content=data,
                content_type=content_type
            )
            crud_message.create(msg_data, db=db)
            await manager.send_message(
                client_id=client_id,
                msg_type=Constants.MESSAGE_TYPE_TEXT,
                message=data
            )
    except WebSocketDisconnect:
        manager.disconnect(agent_id)




@router.get("/ws")
async def test_():
    await manager.broadcast("sending test message")
    