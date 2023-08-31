
from fastapi import FastAPI
import logging
import inspect
import os
import sys
import time
from sql_app.database import SessionLocal,engine
import aux.startup as Startup
from routers import users, chat
from sql_app import models

# import from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# Logger
logging.basicConfig(
    format="%(module)-15s:%(levelname)-10s| %(message)s",
    level=logging.INFO
)



app = FastAPI(
    title="ChatBot API"
)
# __init__
@app.on_event("startup")
async def startup_event():

    # Load Config
    ret, message = Startup.load_config()
    if not ret:
        logging.critical(message)
        return exit(1)

    # Connect to Database
    MODELS_INITIALIZED = False
    for i in range(10):
        try:
            models.Base.metadata.create_all(bind=engine)
            MODELS_INITIALIZED = True
            break
        except Exception as e:
            logging.warning(f"entering..{e}")
            time.sleep(10)
        
    if not MODELS_INITIALIZED:
        exit(2)
    
    db = SessionLocal()
    #create initial data

    app.include_router(users.router)
    app.include_router(chat.router)


